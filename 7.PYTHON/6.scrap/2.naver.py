import requests
from bs4 import BeautifulSoup

url = "https://www.naver.com/"

resp = requests.get(url)
resp.encoding = "utf-8"
if (resp.status_code == 200):
    print(resp.text)
else:
    print("해당 페이지를 가져오는데 실패했습니다. code: ", resp.status_code)

soup = BeautifulSoup(resp.text, "html.parser")