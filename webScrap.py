import requests
from bs4 import BeautifulSoup

brochures = []

url = "https://www.prospektmaschine.de/hypermarkte/"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')

allCatalogues = soup.find_all("div", class_="brochure-thumb")

for div in allCatalogues:
    titleTag = div.find("strong")
    title = titleTag.text.strip() if titleTag else "Unknown"

    logoTag = div.find("img", class_="lazyloadLogo")
    shopName = logoTag["alt"].replace("Logo ", "") if logoTag else "Unknown"
