from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
# import os
import math
from selenium.webdriver.support.wait import WebDriverWait






# Instantiate options
# opts = Options()

# Set the location of the webdriver
#chrome_driver = os.getcwd() + "\chromedriver.exe"

# initialize document
def document_initialized(driver):

    # Parse processed webpage with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, features="html5lib")
    #print(soup.prettify())
    # with open("output.txt", "w") as file:
    #     file.write(soup.prettify())

    # Step 1b: Extracting the data
    body = soup.find("body")
    div_1 = body.find("div", id="__next")
    #print(div_1.prettify())
    div_2 = div_1.find("div")
    #print(div_2.prettify())
    # with open("output.txt", "w") as file:
    #     file.write(div_2.prettify())
        
    main_tag = div_2.find("main", class_ = "fill-vertical-space")
    #print(main)
    # with open("output.txt", "w") as file:
    #     file.write(main.prettify())
    div_3 = main_tag.find("div", class_="grid-12 Search_productsPage__e_PFE")
    #print(div_3.prettify())
    # with open("output.txt", "w") as file:
    #     file.write(div_3.prettify())

    return div_3

def document_initialized_2(driver):
    soup = BeautifulSoup(driver.page_source, features="html5lib")
    #print(soup.prettify())
    # with open("output.txt", "w") as file:
    #     file.write(soup.prettify())

    # Step 2: Extracting the data
    body = soup.find("body")
    div_1 = body.find("div", id="__next")
    #print(div_1.prettify())
    div_2 = div_1.find("div")
    #print(div_2.prettify())
    # with open("output.txt", "w") as file:
    #     file.write(div_2.prettify())
        
    main = div_2.find("main")
    #print(main)
    # with open("output.txt", "w") as file:
    #     file.write(main.prettify())
    div_3 = main.find("div")
    #print(div_3.prettify())
    # with open("output.txt", "w") as file:
    #     file.write(div_3.prettify())
    div_4 = div_3.find("div", class_="col-9 grid-9 col-m-big-12")
    # with open("output.txt", "w") as file:
    #     file.write(div_4.prettify())
    #print(div_4)
    div_5 = div_4.find("div", class_="col-7 col-l-9 col-start-l-1 col-start-2")
    return div_5    

# Instantiate a webdriver
driver = webdriver.Chrome()
driver.get("https://www.lulu.com/search?page=1&q=jews&pageSize=100&adult_audience_rating=00")
u = WebDriverWait(driver, timeout=10).until(document_initialized)


def page_scraper(page):
    # Load the HTML page
    driver.get(page)
    v = WebDriverWait(driver, timeout=10).until(document_initialized_2)
    print("v")
    print(v)
    # Parse processed webpage with BeautifulSoup
    soup = BeautifulSoup(v.page_source, features="html5lib")
    #print(soup.prettify())
    # with open("output.txt", "w") as file:
    #     file.write(soup.prettify())

    # # Step 2: Extracting the data
    # body = soup.find("body")
    # div_1 = body.find("div", id="__next")
    # #print(div_1.prettify())
    # div_2 = div_1.find("div")
    # #print(div_2.prettify())
    # # with open("output.txt", "w") as file:
    # #     file.write(div_2.prettify())
        
    # main = div_2.find("main")
    # #print(main)
    # # with open("output.txt", "w") as file:
    # #     file.write(main.prettify())
    # div_3 = main.find("div")
    # #print(div_3.prettify())
    # # with open("output.txt", "w") as file:
    # #     file.write(div_3.prettify())
    # div_4 = div_3.find("div", class_="col-9 grid-9 col-m-big-12")
    # # with open("output.txt", "w") as file:
    # #     file.write(div_4.prettify())
    # #print(div_4)
    # div_5 = div_4.find("div", class_="col-7 col-l-9 col-start-l-1 col-start-2")
    # #print(div_5)
    # # with open("output.txt", "w") as file:
    # #     file.write(div_5.prettify())
    link_texts = soup.find_all("h3")

    links = []
    for link_text in link_texts:
        links.append("https://www.lulu.com/" + link_text.find("a")["href"])

    # Write links into a file
    for link in links:
        with open("links.txt", "a") as file:
            file.write(link)


# Step 1a: Load the webpage to get the number of pages


# Parse processed webpage with BeautifulSoup
print(u.page_source)
soup = BeautifulSoup(u.page_source)
# #print(soup.prettify())
# # with open("output.txt", "w") as file:
# #     file.write(soup.prettify())

# # Step 1b: Extracting the data
# body = soup.find("body")
# div_1 = body.find("div", id="__next")
# #print(div_1.prettify())
# div_2 = div_1.find("div")
# #print(div_2.prettify())
# # with open("output.txt", "w") as file:
# #     file.write(div_2.prettify())
    
# main_tag = div_2.find("main", class_ = "fill-vertical-space")
# #print(main)
# # with open("output.txt", "w") as file:
# #     file.write(main.prettify())
# div_3 = main_tag.find("div", class_="grid-12 Search_productsPage__e_PFE")
# #print(div_3.prettify())
# # with open("output.txt", "w") as file:
# #     file.write(div_3.prettify())
# div_4 = div_3.find("div", class_="col-9 grid-9 col-m-big-12")

# Find the number of pages
div_4 = soup.find("div", class_="col-9 grid-9 col-m-big-12")
number = div_4.find("div", class_="SortBar_sortBar__info__Njt_r")
ind_of = number.text.index("of") + 3
rest = number.text[ind_of:]
ind_space = rest.index(" ")
num_books = int(rest[:ind_space])
num_pages = math.ceil(num_books / 100)
print(num_pages)


# TODO: Area of improvement by increasing the number of books per page

# Iterate over every page
for i in range(1, num_pages + 1):
    # Load the HTML page
    page = "https://www.lulu.com/search?page=" + str(i) + "&q=jews&pageSize=100&adult_audience_rating=00"
    page_scraper(page)




