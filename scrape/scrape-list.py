from bs4 import BeautifulSoup
import requests

html = requests.get("https://www.lulu.com/search?page=1&q=jews&pageSize=10&adult_audience_rating=00")
soup = BeautifulSoup(html.content, "html.parser")


body = soup.find("body")
div_1 = body.find("div")
div_2 = div_1.find("div")
main = div_2.find("main")
print(main)
div_3 = main.find("div")
#print(div_3)
#div_4 = div_3.find("div")
#print(div_4)
# div_5 = div_4.find_all("div")[1]


#print(div_5)

# for result in results:
#     print(result)

