from scrape_list import scrape_search_term
from scrape_entry import scrape_url
import os
import pandas as pd


# # TODO: Handle the multiple words search term

search_term = "louis ginzberg" 

search_term = search_term.replace(" ", "+")

all_links = scrape_search_term(search_term)

for link in all_links:
    scrape_url(link, search_term)

# scrape_url("https://www.lulu.com/shop/apostle-arne-horn/the-book-of-enoch/paperback/product-1mwr4gdv.html?q=jews", "outlier3")


# Read a file and store ISBN or URL. Check if ISBN already exists. If it does, check URL. If not, add that book

# Check if file exists in the operating system
file_name = search_term + ".csv"
if os.path.isfile(file_name):
    df = pd.read_csv(file_name)
    ISBN_col = df["ISBN"]
    ISBN_set = set(ISBN_col)
    URL_col = df["URL"]
    URL_set = set(URL_col)

# Open file
