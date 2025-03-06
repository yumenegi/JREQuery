import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import datetime
import json


url = "https://ekitan.com/timetable/railway/line-station/151-0/d1?view=list"
eki = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(eki.content, "html.parser")

active = soup.find("div", class_="active")

eki_ueno_yama = active.find_all("li", class_="ek-narrow")
euy = [info.get_text().strip() for info in eki_ueno_yama]
euy = [i.split('\n') for i in euy]

# Remove Empty String
for i, y in enumerate(euy):
    euy[i] = list(filter(None, map(str.strip, y)))

# for i in euy:
#     print(i)

t = datetime.datetime.now(datetime.timezone.utc)
t += datetime.timedelta(hours=9)

for i, it in enumerate(euy):
    train_t = it[0].split(':')
    # print(train_t)
    if (int(train_t[0]) >= t.hour and int(train_t[1]) >= t.minute):
        break

for i in euy[i:i+8]:
    print(" | ".join(i))


class Ekitan:
    def __init__(self, line:str):
        """Make request to Ekitan and set up information needed to query the information
        of a train line"""
        pass

    def get_timetable_by_id(self, station_id:int):
        pass
    
    def get_timetable_by_name(self, station:str):
        pass

