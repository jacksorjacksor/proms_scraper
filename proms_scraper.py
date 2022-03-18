import requests

html = requests.get("https://www.bbc.co.uk/proms/events/by/date/2021").content

print(html)