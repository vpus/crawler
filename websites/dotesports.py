from datetime import datetime, timezone

from clients.firestore import Firestore

class Dotesports():
    def __init__(self, browser):
        self.browser = browser
#         self.firestore = Firestore()
        
    def crawl(self):
        self.browser.get("https://www.dotesports.com")
        articles = self.browser.find_elements_by_tag_name("article")
        article_data_list = []
        for article in articles:
            article_data = self.extract_data(article)
            article_data_list.append(article_data)
            
        return article_data_list
        
    def extract_data(self, article):
        article_data = {}
        article_data["is_original"] = False
        article_data["author"] = article.find_element_by_class_name("author").text
        article_data["author-nicename"] = article.find_elements_by_class_name("author")[1].get_attribute("href")
        article_data["thumbnail"] = article.find_element_by_tag_name("img").get_attribute("src")
        article_data["link"] = article.find_element_by_css_selector("a").get_attribute("href")
        post_time = article.find_element_by_tag_name("time").get_attribute("datetime")
        parsed_datetime = datetime.strptime(post_time, "%Y-%m-%dT%H:%M:%S%z")
        article_data["date_gmt"] = int(parsed_datetime.replace(tzinfo=timezone.utc).timestamp())
        article_data["summary"] = article.find_element_by_css_selector("p").text
        article_data["title"] = article.find_element_by_class_name("entry-title").text
        categories = article.find_element_by_class_name("post-categories")
        for category in categories.find_elements_by_css_selector("li"):
            article_data["category"] = category.text
            # TODO: support multiple category
            break
        return article_data
    
    