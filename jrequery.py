import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from enum import Enum
from dataclasses import dataclass

RegionList = ["kanto", "shinetsu", "tohoku", "chyokyori", "shinkansen"]


class JREStatus:
    _JREQResults = {}
    _JREQAvail = {}
    
    def __init__(self, debug=False):
        # Make request to query all JR East operational regions to get info
        # of all regions
        for region in RegionList:
            r = requests.get(
                "https://traininfo.jreast.co.jp/train_info/%s.aspx" % region, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            # Parse with BS4
            soup = BeautifulSoup(r.content, 'html.parser')

            # Find all line names
            s = soup.find_all('span', class_='name')
            JRELines = [line.get_text().strip() for line in s]

            # Add to available lines
            self._JREQAvail[region] = JRELines

            # Find all info corresponding to each line
            s = soup.find_all('div', class_='rosen_infoBox')
            JRENotices = [info.get_text().strip() for info in s]

            # Make sure all lines have corresponding information
            assert len(JRELines) == len(JRENotices)

            # Parse all found info into _JREQResults dictionary
            self._JREQResults[region] = {}
            for i, j in zip(JRELines, JRENotices):
                if (i not in self._JREQResults[region].keys()):
                    self._JREQResults[region][i] = j.replace("\n\n","：")

            # If debugging enabled, print all information found
            if (debug):
                for key, val in self._JREQResults[region].items():
                    print("%s: %s" % (Fore.RED + key if val != "平常運転" else Fore.GREEN+key, val))

    def get_all_stats(self, region, debug = False) -> dict:
        return self._JREQResults[region]
    
    def get_stats(self, line, region) -> str:
        if line in self._JREQResults[region].keys():
            return self._JREQResults[region][line]
        else:
            raise Exception("The line queried does not exist. 問い合わせた列車路線は存在しない。")
    
    def get_all_avail(self) -> dict:
        return self._JREQAvail

    def is_avail(self, line, region) -> bool:
        return line in self._JREQAvail[region]

    def is_normal(self, line, region) -> bool:
        if line in self._JREQResults[region].keys():
            return True if self._JREQResults[region][line] == "平常運転" else False
        else:
            raise Exception("The line queried does not exist. 問い合わせた列車路線は存在しない。")
        
class JRETimetable:
    # TODO: Query Ekitan for timetable given line and station
    def get(line, station):
        pass