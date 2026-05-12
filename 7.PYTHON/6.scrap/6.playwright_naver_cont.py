
from playwright.sync_api import sync_playwright
import csv

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://news.naver.com/section/105")

    titles = page.locator(".section_article.as_headline a.sa_text_title")

    links = []

    for i in range(titles.count()):
        news = titles.nth(i)

        title = news.inner_text().strip()

        href = news.get_attribute("href")

        links.append({
            "title": title,
            "href": href
        })

    for news in links:
        print("-" * 60)
        print("제목: ", news["title"])
        print("링크:", news["href"] )
    browser.close()
