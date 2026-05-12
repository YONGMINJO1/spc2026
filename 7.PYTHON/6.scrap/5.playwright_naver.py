
from playwright.sync_api import sync_playwright
import csv

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://news.naver.com/section/105")

    titles = page.locator(".section_article.as_headline a.sa_text_title")

    for i in range(titles.count()):
        news = titles.nth(i)

        text = news.inner_text().strip()

        link = news.get_attribute("href")

        print(text)
        print(link)
        print("-" * 30)
    # texts = titles.all_text_contents()
    #print(title.count())
    browser.close()

# with open("news.csv", "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)

#     for newtext in texts:
#         writer.writerow([newtext])