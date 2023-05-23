from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os


# Instantiate options
opts = Options()
opts.headless = True

# Set the location of the webdriver
chrome_driver = os.getcwd() + "chromedriver"

# Instantiate a webdriver
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

# Load the HTML page
driver.get("https://www.lulu.com/search?page=1&q=jews&pageSize=10&adult_audience_rating=00")

# Parse processed webpage with BeautifulSoup
soup = BeautifulSoup(driver.page_source)
print(soup.prettify())