from scrape_list import scrape_search_term
from scrape_entry import scrape_url
import os
import pandas as pd


search_term = "Walder" 

search_term = search_term.replace(" ", "+")

# Get all book UERLs
all_links = scrape_search_term(search_term)

# Check if file already exists in the operating system
file_name = search_term + ".csv"

if os.path.isfile(file_name):
    df = pd.read_csv(file_name)
    ISBN_col = df["ISBN"]
    ISBN_set = set(ISBN_col)
    URL_col = df["URL"]
    URL_set = set(URL_col)

    for link in all_links:
        scrape_url(link, search_term, True, ISBN_set, URL_set)

else:
    for link in all_links:
        scrape_url(link, search_term, False)
# Open file
