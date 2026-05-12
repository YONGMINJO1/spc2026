import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.naver.com/"

resp = requests.get(url)
resp.encoding = "utf-8"

soup = BeautifulSoup(resp.text, "html.parser")
print(soup)

news = soup.select(".MediaNewsView-module_desc_list__uQ3r1")
print(news)