from scrape_list import scrape_search_term
from scrape_entry import scrape_url
import pandas as pd

def search(search_term, upload_file):
    search_term = search_term.replace(" ", "+")

    # Get all book UERLs
    all_links = scrape_search_term(search_term, 0)

    if not all_links:
        return
    # TODO: Do some error handling for non-CSV files
    df = pd.read_csv(upload_file)
    ISBN_col = df["ISBN"]
    ISBN_set = set(ISBN_col)
    URL_col = df["URL"]
    URL_set = set(URL_col)

    for link in all_links:
        scrape_url(link, upload_file, search_term, ISBN_set, URL_set)
