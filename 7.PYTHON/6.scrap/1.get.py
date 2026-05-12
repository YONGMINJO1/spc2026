# 1. books.toscrape.com 에 접속해서 페이지를 받아온다
# 2. DOM 을 bs4로 구성한다
# 3. 첫 페이지의 도서명, 평점, 가격을 받아온다
# 4. CSV파일로 저장한다.

import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"

resp = requests.get(url)
if (resp.status_code == 200):
    print(resp.text)
else:
    print("해당 페이지를 가져오는데 실패했습니다. code: ", resp.status_code)

soup = BeautifulSoup(resp.text, "html.parser")

# print(soup)
# books = soup.find_all("article", class_="product_pod")
books = soup.select("article.product_pod") # article이면서 product_pod 클래스가 붙은애만 골라줘

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5

}

with open("books.csv", "w", encoding="utf-8",newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow({"도서명","평점","가격"})

for book in books:
    # print(book)
    # break
    # print(title)
    title = book.h3.a['title']

    # 평점...
    rating = book.p["class"][1]
    rating_num = rating_map[rating]

    # 가격...
    price = book.select_one(".price_color").text
    price = price.replace("£", "")

    # print(f"도서명: {title}, 평점 : {rating}, 가격: {price}")
    csv_writer.writerow({title,rating,price})

print("파일작성완료")