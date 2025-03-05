import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

x = requests.get("https://traininfo.jreast.co.jp/train_info/tohoku.aspx", headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(x.content, 'html.parser')

s = soup.find_all('span', class_='name')
JRELines = [line.get_text().strip() for line in s]

s = soup.find_all('div', class_='rosen_infoBox')
JRENotices = [info.get_text().strip() for info in s]

JREQuery = {}
for i, j in zip(JRELines, JRENotices):
    if (i not in JREQuery.keys()):
        JREQuery[i] = j.replace("\n\n","：")

for key, val in JREQuery.items():
    print("%s: %s" % (Fore.RED + key if val != "平常運転" else Fore.GREEN+key, val))
# print(JREQuery)