from datetime import datetime, timezone

# from clients.firestore import Firestore

class Gosugamers():
    def __init__(self, browser):
        self.browser = browser
#         self.firestore = Firestore()
        
    def crawl(self):
        self.browser.get("https://www.gosugamers.net/articles")
        articles = self.browser.find_element_by_id("articles").find_elements_by_tag_name("article")
        article_data_list = []
        for article in articles:
            article_data = self.extract_data(article)
            if len(article_data) != 0:
                article_data_list.append(article_data)
            
        return article_data_list
        
    def extract_data(self, article):
        article_data = {}
        article_data["is_original"] = False
        post_details = article.find_element_by_class_name("post-details").text
        post_details_split = post_details.split("\n")
        if len(post_details_split) != 3:
            return {}
        category, _, author  = post_details_split
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
    
    