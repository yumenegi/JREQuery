import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from enum import Enum

class JRERegion:
    KANTO = "kanto"
    SHINETSU = "shinetsu"
    TOHOKU = "tohoku"
    CHYOKYORI = "chyokyori"
    SHINKANSEN = "shinkansen"


class JREQuery:
    def JREQuery(region, debug = False) -> dict:
        x = requests.get("https://traininfo.jreast.co.jp/train_info/%s.aspx" % region, headers={'User-Agent': 'Mozilla/5.0'})

        soup = BeautifulSoup(x.content, 'html.parser')

        s = soup.find_all('span', class_='name')
        JRELines = [line.get_text().strip() for line in s]

        s = soup.find_all('div', class_='rosen_infoBox')
        JRENotices = [info.get_text().strip() for info in s]

        res = {}
        for i, j in zip(JRELines, JRENotices):
            if (i not in res.keys()):
                res[i] = j.replace("\n\n","：")

        if (debug):
            for key, val in res.items():
                print("%s: %s" % (Fore.RED + key if val != "平常運転" else Fore.GREEN+key, val))
        return res