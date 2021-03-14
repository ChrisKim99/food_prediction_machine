import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv


# setting webdriver
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

driver = webdriver.Chrome("C:/Users/Lenovo/PS/django_projects/cse487_project1/chromedriver.exe", options=options)
driver.maximize_window()

# loading page
url = "https://www.food.com/recipe?ref=nav"
driver.get(url)

# scrolling down to the end bottom point
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

elem = driver.find_element_by_class_name("gk-aa-load-more")
elem.click()

prev_height = driver.execute_script("return document.body.scrollHeight")

# each page contains 10 items

page = 2 # number of page to load
end = False

#load the 1000 page which contains 10000 food items
while (page < 1000 or end == True):
    
    try:
        # find the first item of each loading page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-sf-pn={}]".format(page))))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        curr_height = driver.execute_script("return document.body.scrollHeight")
        if(curr_height == prev_height):
            end = True
            break
        else:
            prev_height = curr_height
        page += 1
        print(page)
    except:
        print("re-try")
        continue
    
print("Loading pages are done")
driver.get_screenshot_as_file("./cse487_project1/food_page.png")


# since the page is loaded, now we can scrap data
soup = BeautifulSoup(driver.page_source, "lxml")

# beautiful soup to scrap all food items
items = soup.find("div", attrs={"class":"tile-stream clearfix fdStream"}).find_all("h2", attrs={"class":"title"})

# setting up file to store recipe data
filename = "./cse487_project1/data/recipe/1_recipe.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") # 줄바꿈 없앰
writer_ingredients = csv.writer(f)

# setting up file to store nutrition data
filename = "./cse487_project1/data/nutrition/1_nutrition.csv"
g = open(filename, "w", encoding="utf-8-sig", newline="")
writer_ntr = csv.writer(g)

# headers of nutrition data
header_of_ntr = ["title", "calories", "calories from fat(g)", "total fat(g)","saturated fat(g)", "cholesterol(mg)","sodium(mg)", "total carbohydrate(g)","dietary fiber(g)","sugar(g)","protein(g)"]
#["title", "calories", "calories from fat", "total fat","saturated fat", "cholesterol","sodium", "total carbohydrate","dietary fiber","sugar","protein"]
writer_ntr.writerow(header_of_ntr)



# iterating each food item
for item in items:

    url = item.a["href"]

    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    # food title
    title = soup.find("div", attrs = {"class":"recipe-title"}).get_text()

    # recipe data of the current food
    recipes = soup.find("ul", attrs={"class":"recipe-ingredients__list"}).find_all("div", attrs={"class":"recipe-ingredients__ingredient-parts"})
    
    food_ingredient_row = [] #food name and ingredients row

    food_ingredient_row.append(title)

    for recipe in recipes:
    
        if(recipe.a):
            food_ingredient_row.append(recipe.a.get_text())
            
        else:
            text = recipe.get_text().strip()
            food_ingredient_row.append(text)
            
    # store recipe data        
    writer_ingredients.writerow(food_ingredient_row)
    

    # nutrition data of the current food
    ntr = soup.find("section", attrs={"class":"recipe-nutrition__info"}).find_all("p", attrs={"class":re.compile("^recipe-nutrition__item")})
    
    ntr_list = []
    
    ntr_list.append(title)
    for nt in ntr:
        if not (nt.span):
            ntr_list.append(nt.get_text())
        else:
            ntr_list.append(nt.span.get_text())  

    # store nutrition data 
    writer_ntr.writerow(ntr_list)

print("work is done")

    