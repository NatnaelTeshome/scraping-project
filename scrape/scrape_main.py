from scrape_list import scrape_search_term
from scrape_entry import scrape_url

# TODO: Handle the multiple words search term


all_links = scrape_search_term("jews")

for link in all_links:
    scrape_url(link, "jews")

