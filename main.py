from datetime import datetime, timezone
import hashlib

import firebase_admin
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import websites

def hash_url(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def send_2_firestore(article_data, force_update = False):
    try:
        url_hashed = hash_url(article_data["link"])
        article_ref = db.collection(u"articles").document(url_hashed)
        if article_ref.get().exists and not force_update:
            print("Article {} already exists!".format(article_data["link"]))
        else:
            print("Sending Article {}".format(article_data["link"]))
            # update article
            article_ref.set(article_data)

            # update category
            category_ref = db.collection(u"categories").document(article_data["category"]).collection(u"articles").document(url_hashed)
            category_ref.set(article_data)

            # update author
            author_ref = db.collection(u"authors").document(article_data["author"]).collection(u"articles").document(url_hashed)
            author_ref.set(article_data)
    except Exception as e:
        print("Failed to send article to Firestore: {}\nArticle Data:\n{}".format(e, article_data))

def extract_data_gosugamers(article):
    article_data = {}
    article_data["is_original"] = False
    post_details = article.find_element_by_class_name("post-details").text
    category, _, author  = post_details.split("\n")
    article_data["author"] = author
    article_data["author-nicename"] = ""
    article_data["thumbnail"] = article.find_element_by_tag_name("img").get_attribute("src")
    article_data["link"] = article.find_element_by_css_selector("a").get_attribute("href")
    post_time = article.find_element_by_tag_name("time").get_attribute("datetime")
    parsed_datetime = datetime.strptime(post_time, "%Y-%m-%dT%H:%M:%S%z")
    article_data["date_gmt"] = int(parsed_datetime.replace(tzinfo=timezone.utc).timestamp())
    article_data["summary"] = article.find_element_by_class_name("post-excerpt").text
    article_data["title"] = article.find_element_by_class_name("post-title").text
    article_data["category"] = category
    return article_data

cred = credentials.Certificate("../firestore-tryout/vpesports-221908-firebase-adminsdk-7o81s-9761f6a469.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

browser = webdriver.Chrome("chromedriver/chromedriver", options=options)

# dotesports
dotesports = websites.Dotesports(browser)
dotesports_data = dotesports.crawl()
for article in dotesports_data:
    send_2_firestore(article)

# gosugamers
gosugamers = websites.Gosugamers(browser)
gosugamers_data = gosugamers.crawl()
for article in gosugamers_data:
    send_2_firestore(article)