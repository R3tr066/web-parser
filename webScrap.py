import requests
from bs4 import BeautifulSoup

url = str(input("Insert url: "))
# Making a GET request
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')

cataloge = soup.find("div", {"class": "letaky-grid"})
print(cataloge.prettify())
