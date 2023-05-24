from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import os


# Instantiate options
# opts = Options()

# Set the location of the webdriver
#chrome_driver = os.getcwd() + "\chromedriver.exe"

# Instantiate a webdriver
driver = webdriver.Chrome()

# Load the HTML page
driver.get("https://www.lulu.com/search?page=2&q=jews&pageSize=10&adult_audience_rating=00")


# Parse processed webpage with BeautifulSoup
soup = BeautifulSoup(driver.page_source)
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
#print(div_5)
with open("output.txt", "w") as file:
     file.write(div_5.prettify())
link_texts = div_5.find_all("h3")

for link_text in link_texts:
    print(link_text.find("a")["href"])

