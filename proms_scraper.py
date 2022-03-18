import csv
import requests
from bs4 import BeautifulSoup

with open("proms_composer_data.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f,delimiter='|')
    for year in range(1895,2022):
        url = f"https://www.bbc.co.uk/proms/events/by/date/{year}"
        html = requests.get(url).content
        soup = BeautifulSoup(html, "lxml")
        query_tree = soup.find_all("a", class_="ev-act-schedule__artist-name")
        writer.writerow([str(year)] + [item.text for item in query_tree if "composer" in item.attrs["href"]])