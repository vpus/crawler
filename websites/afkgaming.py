from datetime import datetime, timezone

class Afkgaming():
    def __init__(self, browser) -> None:
        self.browser = browser

    def crawl(self):
        self.browser.get("https://afkgaming.com/")
        articles = self.browser.find_element_by_id("")