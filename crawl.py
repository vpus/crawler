from datetime import datetime, timezone
import hashlib

import firebase_admin
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import websites
import utils.category_parser

cred = credentials.Certificate("configs/firebase-service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def hash_url(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def send_2_firestore(article_data, force_update=False):
    try:
        url_hashed = hash_url(article_data["link"])
        article_ref = db.collection(u"articles").document(url_hashed)
        if article_ref.get().exists and not force_update:
            print("Article {} already exists!".format(article_data["link"]))
        else:
            # update article
            article_ref.set(article_data)

            # update category
            category = article_data["category"]
            parsed_category_list = utils.category_parser.parse(category)
            print("Sending {} Article {}".format(parsed_category_list, article_data["link"]))
            for parsed_category in parsed_category_list:
                category_ref = db.collection(u"categories").document(
                    parsed_category).collection(u"articles").document(
                        url_hashed)
                category_ref.set(article_data)

            # update author
            author_ref = db.collection(u"authors").document(
                article_data["author"]).collection(u"articles").document(
                    url_hashed)
            author_ref.set(article_data)
    except Exception as e:
        print("Failed to send article to Firestore: {}\nArticle Data:\n{}".
              format(e, article_data))

def run():
    # Check VPEsports Original
    print("Fetching VPEsports...")
    vpesports = websites.VPEsports()
    vpesports_data = vpesports.crawl()
    for article in vpesports_data:
        send_2_firestore(article)

    print("Starting up Browser...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    browser = webdriver.Chrome("chromedriver/chromedriver", options=options)

    # dotesports
    print("Crawling Dotesports...")
    dotesports = websites.Dotesports(browser)
    dotesports_data = dotesports.crawl()
    for article in dotesports_data:
        send_2_firestore(article)

    # # gosugamers
    print("Crawling Gosugamers")
    gosugamers = websites.Gosugamers(browser)
    gosugamers_data = gosugamers.crawl()
    for article in gosugamers_data:
        send_2_firestore(article)

    # trackdota
    print("Crawling TrackDota")
    trackdota = websites.Trackdota(browser)
    trackdota_data = trackdota.crawl()
    for article in trackdota_data:
        send_2_firestore(article, force_update=True)

if __name__ == "__main__":
    run()