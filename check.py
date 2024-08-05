from playwright.sync_api import sync_playwright
from time import sleep


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://geonode.com/free-proxy-list")
    while True:
        proxies
