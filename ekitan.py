import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

eki = requests.get("https://ekitan.com/timetable/railway/line-station/182-11/d2?view=list", headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(eki.content, "html.parser")

active = soup.find("div", class_="active")

eki_ueno_yama = active.find_all("li", class_="ek-narrow")
euy = [info.get_text().strip() for info in eki_ueno_yama]
euy = [i.split('\n') for i in euy]

# Remove Empty String
for i, y in enumerate(euy):
    euy[i] = list(filter(None, map(str.strip, y)))

for i in euy:
    print(i)