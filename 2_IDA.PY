import pandas as pd
import csv
import numpy as np
import string
import math
import re

# count max number of items to fill headers
def count_max(filename):
    f = open(filename, 'r')
    lines = csv.reader(f)
    max = 0
    for line in lines:
        if (max < len(line)):
            max = len(line)
    return max

# create headers using count_max function
def create_header(filename):
    new_file = "./cse487_project1/data/recipe/2_recipe_with_header.csv"
    
    # count max len of items
    len = count_max(filename)
     
    with open(filename, 'r', encoding='utf-8-sig') as f_out, \
         open(new_file, 'w', newline="", encoding='utf-8-sig') as f_in:


        writer = csv.writer(f_in)
        header = ["title"]

        # create a header list filled with number of items
        for idx in range(len - 1):
            header.append("item{}".format(idx + 1))

        # write header
        writer.writerow(header)

        # copy paste rows of data into new file
        for line in csv.reader(f_out):

            writer.writerow(line)

create_header("./cse487_project1/data/recipe/1_recipe.csv")

# we have proper header now, but we need to fill blanks of each row if corresponding items are empty
def fill_blank(filename):

    new_file = "./cse487_project1/data/recipe/3_recipe_with_comma.csv"

    # max number of items
    cnt = count_max(filename)

    with open(filename, 'r') as reader,\
        open(new_file, 'w',  newline="") as writer:
        
        lines = csv.reader(reader, delimiter = ",")
        
        header = next(lines)
        
        writer = csv.writer(writer)
        
        writer.writerow(header)
        
        for line in lines:
            
            if(len(line) < cnt):
                freq = cnt - len(line)
                while(freq != 0):
                    line.append('$')
                    freq -= 1
            
            writer.writerow(line)
            #12
#fill_blank("./cse487_project1/data/recipe/2_recipe_with_header.csv")


# 3
def remove_front_space(text):
    answer = ""                    
    for n in range(len(text)):
        if(text[n] == ' ' and text[n+1] == ' '):
            count = n + 1
            while(text[count] == ' '):
                count += 1
            answer = text[count:len(text)]
    if(answer == ""):
        answer = text
        
    if(answer[0] == "(" and answer[len(answer)-1] == ")"):
        answer = '$'

    return answer

def remove_back_space(text):
    answer = ""
    if(text == 0):
        answer=0
    else:
        for n in range(len(text)):
            if(text[n] == ' ' and text[n + 1] == '('):
                answer = text[0:n]
                break
            if(text[n] == ','):
                answer = text[0:n]
                break
        if(answer == ""):
            answer = text
    return answer

# remove unwanted space for items
def remove_space(filename):

    new_file = "./cse487_project1/data/recipe/4_recipe_with_no_space.csv"
    data = pd.read_csv(filename)

    header = data.columns.values

    header_with_no_title = np.delete(header,0)

    for header in header_with_no_title:

        for idx in range(len(data[header])):
            
            data[header][idx] = remove_back_space(remove_front_space(data[header][idx]))
            
    data.to_csv(new_file, index = False)

#remove_space("./cse487_project1/data/recipe/3_recipe_with_comma.csv")

# remove duplicated items for each row
def duplicate(filename):
    df = pd.read_csv(filename)

    height = df.shape[0]
    width = df.shape[1]
    
    fields = []
    for i in range(width-1):
        fields.append("item{}".format(i+1))   

    for row in range(height):
        items = set()
        
        for field in fields:
            if(df[field][row] != '$' and df[field][row] != "half-and-half"):
                items.add(df[field][row])
        
        items_len = len(items)

        inc_to_items_len = 0


        for field, item in zip(fields, items):
            df[field][row] = item

        for field in fields:
            if(inc_to_items_len < items_len):
                inc_to_items_len += 1
            else:
                df[field][row] = '$'

        
    df.to_csv("./cse487_project1/data/recipe/5_recipe_no_duplicate.csv", index=False)
#duplicate( "./cse487_project1/data/recipe/4_recipe_with_no_space.csv")


def helper_non_char(text):

    # remove quotation
    if not ',' in text:
        text = text.replace('"',"")

    # remove parenthesis
    text = re.sub(r" ?\([^)]+\)", "", text)

    # remove common unwanted symbol
    text = text.replace('-'," ").replace('!',"").replace('.'," ")

    # remove unwanted whitesapce
    text = text.strip()
    text = re.sub(' +', ' ', text)

    return text    


def remove_non_char(filename):

    new_file = "./cse487_project1/data/recipe/6_recipe_without_nonchar.csv"
    data = pd.read_csv(filename)

    
    for idx in range(len(data["title"])):

        data["title"][idx] = helper_non_char(data["title"][idx])
            
    data.to_csv(new_file, index = False)


#remove_non_char("./cse487_project1/data/recipe/5_recipe_no_duplicate.csv")

# 5

def sorting(filename):
    
    df = pd.read_csv(filename)

    df.sort_values('title', inplace=True)

    height = df.shape[0]
    width = df.shape[1]
    
    fields = []
    for i in range(width-1):
        fields.append("item{}".format(i+1))   

    for row in range(height):
        dict_holder = {}
        
        for key in list(string.ascii_lowercase):
            dict_holder[key] = []
            for field in fields:
                if(key == df[field][row][0]):
                    dict_holder[key].append(df[field][row])
        items = []
        for li in dict_holder.values():
            if(len(li) != 0):
                for item in li:
                    items.append(item)
        
    
        for field, item in zip(fields, items):
            df[field][row] = item

        
    df.to_csv("./cse487_project1/data/recipe/final_recipe.csv", index=False)

#sorting("./cse487_project1/data/recipe/6_recipe_without_nonchar.csv")

# 6 

# -------------------------------------------------recipe done ------------------------------------------------
def filter_value(text):
    number = ""
    for let in text:
        if(let.isdigit()):
            number = number + let

    return number
    

def only_value(filename):
    
    new_file = "./cse487_project1/data/nutrition/2_nutrition_only_num.csv"

    data = pd.read_csv(filename)

    header = data.columns.values

    header_with_no_title = np.delete(header,0)

    for header in header_with_no_title:

        for idx in range(len(data[header])):
            
            data[header][idx] = filter_value(data[header][idx]) 

    
    data.to_csv(new_file, index=False)
    

#only_value("./cse487_project1/data/nutrition/1_nutrition.csv")    

#7
def filter_no_cal(filename):
    df = pd.read_csv(filename)

    df = df[df.calories != 0]

    df.to_csv("./cse487_project1/data/nutrition/3_nutrition_all_food.csv", index=False)
    
filter_no_cal("./cse487_project1/data/nutrition/2_nutrition_only_num.csv")


def remove_non_char_ntr(filename):

    new_file = "./cse487_project1/data/nutrition/4_nutrition_without_nonchar.csv"
    data = pd.read_csv(filename)

    
    for idx in range(len(data["title"])):

        data["title"][idx] = helper_non_char(data["title"][idx])
            
    data.to_csv(new_file, index = False)


remove_non_char_ntr("./cse487_project1/data/nutrition/3_nutrition_all_food.csv")

def sort_ntr(filename):
    df = pd.read_csv(filename)

    df.sort_values('title', inplace=True)

    df.to_csv("./cse487_project1/data/nutrition/final_nutrition.csv", index=False)

sort_ntr("./cse487_project1/data/nutrition/4_nutrition_without_nonchar.csv")    

#
#def read_recipe(filename):
#
#    df = pd.read_csv(filename)
#
#    print(df)
#read_recipe("6_recipe_ordered.csv")  