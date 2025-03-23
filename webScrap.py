import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

brochures = []

url = "https://www.prospektmaschine.de/hypermarkte/"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')

allCatalogues = soup.find_all("div", class_="brochure-thumb")

for div in allCatalogues:
    titleTag = div.find("strong")
    title = titleTag.text.strip() if titleTag else "Unknown"

    img_tag = div.find("img")
    if img_tag:
        thumbnail = img_tag.get("src") or img_tag.get("data-src", "")
    else:
        thumbnail = ""

    logoTag = div.find("img", class_="lazyloadLogo")
    shopName = logoTag["alt"].replace("Logo ", "") if logoTag else "Unknown"

    dateTexts = div.find_all("small")

    validFrom, validTo = "", ""

    if dateTexts:
        dateText = dateTexts[0].text.strip()

        if " - " in dateText:
            dateParts = dateText.split(" - ")
            if len(dateParts) == 2:
                validFrom, validTo = dateParts

        elif "von" in dateText:
            match = re.search(r"(\d{2}\.\d{2}\.\d{4})", dateText)
            if match:
                validFrom = match.group(1)
                validTo = ""

    if validFrom:
        validFrom = datetime.strptime(validFrom, "%d.%m.%Y").strftime("%Y-%m-%d")
    if validTo:
        validTo = datetime.strptime(validTo, "%d.%m.%Y").strftime("%Y-%m-%d")


    parsedTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    brochures.append({
        "title": title,
        "thumbnail": thumbnail,
        "shop_name": shopName,
        "valid_from": validFrom,
        "valid_to": validTo,
        "parsed_time": parsedTime
    })

with open("brochures.json", "w", encoding="utf-8") as f:
    json.dump(brochures, f, indent=4, ensure_ascii=False)