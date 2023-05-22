from bs4 import BeautifulSoup
# import requests


import requests

url = "https://www.lulu.com/search?page=2&q=jews&pageSize=10&adult_audience_rating=00"

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}   


response = requests.get(url, headers = headers)
html = response.text

soup = BeautifulSoup(html, "html.parser")

print(soup.prettify())


# html = requests.get(url, headers=headers).text
# print(html)

# soup = BeautifulSoup(html, "html.parser")

# print(soup.prettify())

# body = soup.find("body")
# div_1 = body.find("div")
# div_2 = div_1.find("div")
# main = div_2.find("main")
# print(main)
# div_3 = main.find("div")
#print(div_3)
#div_4 = div_3.find("div")
#print(div_4)
# div_5 = div_4.find_all("div")[1]


#print(div_5)

# for result in results:
#     print(result)
