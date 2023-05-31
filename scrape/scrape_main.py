from scrape_list import scrape_search_term
from scrape_entry import scrape_url

# # TODO: Handle the multiple words search term


all_links = scrape_search_term("jews")

for link in all_links:
    scrape_url(link, "jews_3")

# scrape_url("https://www.lulu.com/shop/apostle-arne-horn/the-book-of-enoch/paperback/product-1mwr4gdv.html?q=jews", "outlier3")