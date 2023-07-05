from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import math
import time


# Create a new instance of the WebDriver

def scrape_search_term(term, times):
    def page_scraper(page):
        # Load the HTML page
        driver.get(page)
        # Parse processed webpage with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, features="html5lib")
        # Step 2: Extracting the data
        body = soup.find("body")
        div_1 = body.find("div", id="__next")
        div_2 = div_1.find("div")     
        main = div_2.find("main")
        div_3 = main.find("div", class_="grid-12 Search_productsPage__e_PFE")
        if not div_3:
            time.sleep(10)
            return page_scraper(page)
        div_4 = div_3.find("div", class_="col-9 grid-9 col-m-big-12")
        div_5 = div_4.find("div", class_="col-7 col-l-9 col-start-l-1 col-start-2")
        link_texts = div_5.find_all("h3")

        links = []
        for link_text in link_texts:
            links.append("https://www.lulu.com/" + link_text.find("a")["href"])


        return links


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    
    # Step 1a: Load the webpage to get the number of pages
    driver.get("https://www.lulu.com/search?page=1&q={}&pageSize=10&adult_audience_rating".format(term))


    # Parse processed webpage with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, features="html5lib")

    # Step 1b: Extracting the data
    div_1 = soup.find("div", id="__next")
    div_2 = div_1.find("div")
    main = div_2.find("main")
    div_3 = main.find("div")
    div_4 = div_3.find("div", class_="col-9 grid-9 col-m-big-12")
    if not div_4:   
        if times == 10:
            return []
        time.sleep(2) 
        return scrape_search_term(term, times + 1)
    # Find the number of pages
    number = div_4.find("div", class_="SortBar_sortBar__info__Njt_r")
    ind_of = number.text.index("of") + 3
    rest = number.text[ind_of:]
    ind_space = rest.index(" ")
    num_books = int(rest[:ind_space])
    num_pages = math.ceil(num_books / 500)

    # TODO: Area of improvement by increasing the number of books per page

    all_links = []
    # Iterate over every page
    for i in range(1, num_pages + 1):
        # Load the HTML page
        page = "https://www.lulu.com/search?page=" + str(i) + "&q={}&pageSize=500&adult_audience_rating".format(term)
        links = page_scraper(page)
        for link in links:
            all_links.append(link)
    
    return all_links



