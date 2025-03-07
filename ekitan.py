import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import datetime
import json


# url = "https://ekitan.com/timetable/railway/line-station/151-0/d1?view=list"
# eki = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
# soup = BeautifulSoup(eki.content, "html.parser")

# active = soup.find("div", class_="active")

# eki_ueno_yama = active.find_all("li", class_="ek-narrow")
# euy = [info.get_text().strip() for info in eki_ueno_yama]
# euy = [i.split('\n') for i in euy]

# # Remove Empty String
# for i, y in enumerate(euy):
#     euy[i] = list(filter(None, map(str.strip, y)))

# # for i in euy:
# #     print(i)

# t = datetime.datetime.now(datetime.timezone.utc)
# t += datetime.timedelta(hours=9)

# for i, it in enumerate(euy):
#     train_t = it[0].split(':')
#     # print(train_t)
#     if (int(train_t[0]) >= t.hour and int(train_t[1]) >= t.minute):
#         break

# for i in euy[i:i+8]:
#     print(" | ".join(i))


EKITAN_URL = "https://ekitan.com"

class Ekitan:
    """
        All time table dictionary is organized as following:
        {
            station (string) : href (list of urls)
        }
    """
    def __init__(self, line:str):
        """Make request to Ekitan and set up information needed to query the information
        of a train line"""
        # Init variables
        self._train = line
        self._time_tb = {}

        # First we need to parse the JSON file that encodes the url of train lines
        # Open File
        with open('ekitan_tt.json') as f:
            line_ids = json.load(f)

        # Find the specific ID
        line_id = line_ids[line]

        self._link = EKITAN_URL + "/timetable/railway/line/%s" % line_id

        r = requests.get(self._link, headers={'User-Agent': 'Mozilla/5.0'})

        soup = BeautifulSoup(r.content, "html.parser")
        tt = soup.find("div", class_="timetable-area")
        tt = tt.find_all("dl", class_="clearfix")

        for t in tt:
            station = t.find("a", {"ga-event-lbl": "GA-TRAC_railway-line_PC_station"}).text
            hrefs = t.find_all("a", {"ga-event-lbl": "GA-TRAC_railway-line_PC_direction"}, href=True)
            self._time_tb[station] = [EKITAN_URL + a["href"] + "?view=list" for a in hrefs]

    def get_all_stations(self):
        return self._time_tb.keys()

    def get_timetable_by_id(self, station_id:int, direction:int):
        # TODO: Implement find by ID
        # Issue: Ekitan Station number does not match JR Station Number
        # Broken up lines that turn into other lines - e.g. Tokyo-Ueno Line
        pass
    
    def get_timetable_by_name(self, station:str, direction:int):
        timetable_link = self._time_tb[station][direction-1]

        r = requests.get(timetable_link, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")

        active = soup.find("div", class_="active")

        timetable_raw = active.find_all("li", class_="ek-narrow")
        timetable = [info.get_text().strip() for info in timetable_raw]
        timetable = [i.split('\n') for i in timetable]

        # Remove Empty String
        for i, y in enumerate(timetable):
            timetable[i] = list(filter(None, map(str.strip, y)))
        return timetable


if __name__ == "__main__":
    eki = Ekitan("中央線")
    print(eki.get_all_stations())
    print(eki.get_timetable_by_name("東京駅", 1))