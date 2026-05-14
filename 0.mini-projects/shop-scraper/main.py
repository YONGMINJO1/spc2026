from playwright.sync_api import sync_playwright

BASE_URL = "https://makemyproject.net/shop"

def main():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(BASE_URL)

        #print(page.title())

        page.wait_for_selector(".card")

        # ca

        browser.close()

main()