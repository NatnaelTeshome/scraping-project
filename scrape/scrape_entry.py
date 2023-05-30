from bs4 import BeautifulSoup
import requests
import csv
import os

# TODO: There could be some specs left: Error handling should be better


def scrape_url(url, filename):


    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    #print(soup.prettify())

    output = {}

    body = soup.find("body")
    div_1 = body.find("div")
    div_2 = div_1.find("div")
    main = div_2.find("main")
    div_3 = main.find("div")
    div_4 = div_3.find("div")
    div_top = div_4.find("div", class_="IntroSection_productPage__intro__aKaZG")
    title_div = div_top.find("div", class_="IntroSection_productPage__intro__details__T4oLR")
    title = title_div.find("h1").text
    output["Title"] = title

    author_p = div_top.find("p", class_="IntroSection_productAuthor__NtGFh")
    # author
    author = author_p.find("a").text
    output["Author"] = author

    type_price_div = div_top.find("div", class_="IntroSection_productPage__intro__details__addToCart__pZ9ec")

    # Type
    type_book = type_price_div.find("p", class_="BookFormatSelectionButton-module_bookFormatHeading__6QMcM").text
    output["Type"] = type_book

    # Price
    price = type_price_div.find("p", class_="BookFormatSelectionButton-module_bookFormatPriceCurrent__GePTd BookFormatSelectionButton-module_bookFormatPrice__cxEWw").text
    output["Price"] = price

    div_bottom = div_4.find("div", class_="grid-12")
    summary = div_bottom.find("div", class_="col-8 col-m-big-12 col-start-m-big-1 col-start-3 ProductDescriptionSection_descriptionContainer__iFXYA").text
    output["Summary"] = summary


    # Details
    div_details = div_bottom.find("div", class_="col-5 col-l-7 col-m-big-10 col-m-10 col-s-11 col-start-3 col-start-m-big-1")
    dl_details = div_details.find("dl", class_="ProductDescriptionSection_specList__ghwp8")

    items_1 = dl_details.find_all("dt")
    descriptions_details = dl_details.find_all("dd")

    print(items_1)
    print(descriptions_details)
    print(type(items_1[0]))

    # Missing fields
    if len(items_1) != 6:
        complete_fields = ["Publication Date", "Language", "ISBN", "Category", "Copyright", "Contributors"]
        items_1_fields = []
        for item in items_1:
            items_1_fields.append(item.text)
        for item in complete_fields:
            if item not in items_1_fields:
                item_string = "<dt> {} </dt>".format(item)
                item_soup = BeautifulSoup(item_string, "html.parser")
                items_1.append(item_soup)
                description_string = "<dd> N/A </dd>"
                description_soup = BeautifulSoup(description_string, "html.parser")
                descriptions_details.append(description_soup)

    for i in range(len(items_1)):
        item = items_1[i].text.strip()
        description = descriptions_details[i].text.strip()
        if item == "Publication Date":
            description = description[-4:]
            output["Publication Year"] = description
            continue
        output[item] = description


    # Specifications
    div_specs = div_bottom.find("div", class_="col-4 col-l-7 col-m-big-10 col-m-10 col-s-11 col-start-l-3 col-start-m-big-1")
    dl_specs = div_specs.find("dl", class_="ProductDescriptionSection_specList__ghwp8")

    items_2 = dl_specs.find_all("dt")
    descriptions_specs = dl_specs.find_all("dd")

    for i in range(len(items_2)):
        item = items_2[i].text.strip()
        description = descriptions_specs[i].text.strip()
        output[item] = description


    div_keyword = div_bottom.find("div", class_="col-8 col-start-3 col-m-big-12 col-start-m-big-1")
    div_keyword_inner = div_keyword.find("div", class_="ProductDescriptionSection_keywords__7RDmG")
    keywords_list = div_keyword_inner.find_all("span")
    clean_keywords = []
    for keyword in keywords_list:
        clean_keywords.append(keyword.text.strip())

    output["Keywords"] = clean_keywords



    # File system
    Column_names = ["Title", "Author", "Type", "Price", "Summary", "Publication Year", "Language", "ISBN", "Category", "Copyright", "Contributors",
    "Pages", "Binding", "Interior Color", "Dimensions", "Format", "Keywords"]

    # Helper function to check if a similar book exists
    # TODO

    # CSV new file writer
    csv_name = "{}.csv".format(filename)
    # if file doesn't exist, create it and write the header
    if not os.path.isfile(csv_name):
        with open(csv_name, 'w') as f:
            csv_obj = csv.DictWriter(f, fieldnames=Column_names)
            csv_obj.writeheader()
            csv_obj.writerow(output)
    # if file exists, append the new entry
    else:
        with open(csv_name, 'a') as f:
            csv_obj = csv.DictWriter(f, fieldnames=Column_names)
            csv_obj.writerow(output)

    # CSV existing file adder
    # csv_name = "Placeholder"
    # with open(csv_name, 'a') as f:
    #     csv_obj = csv.DictWriter(f, fieldnames=Column_names)
        # if checker(output["ISBN"]):
        #     csv_obj.writerow(output)