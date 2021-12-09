from datetime import datetime, timezone

class Trackdota():
    def __init__(self, browser):
        self.browser = browser

    def crawl(self):
        self.browser.get("https://www.trackdota.com/articles")
        articles = self.browser.find_element_by_class_name("t71c1m-0").find_elements_by_class_name("t71c1m-1")
        article_data_list = []
        for article in articles:
            article_data = self._extract_data(article)
            article_data_list.append(article_data)
            
        return article_data_list

    def _extract_data(self, article):
        article_data = {}
        article_data["is_original"] = False
        article_text_splits = article.text.split("\n")
        title = article_text_splits[0]
        time_string = article_text_splits[1]
        tags = article_text_splits[2:]
        article_data["author"] = "TRACKDOTA.COM"
        article_data["author-nicename"] = "TRACKDOTA.COM"

        background_value = article.find_element_by_css_selector("a").value_of_css_property("background")
        url_start = background_value.find("https")
        url_delimiter = background_value[url_start-1]
        url_end = background_value[url_start:].find(url_delimiter)
        article_data["thumbnail"] = background_value[url_start:url_end+url_start]

        article_data["link"] = article.find_element_by_css_selector("a").get_attribute("href")
        # parsed_datetime = datetime.strptime(time_string, "%B %d, %Y")
        parsed_datetime = datetime.strptime(time_string, "%d %B %Y")
        article_data["date_gmt"] = int(parsed_datetime.replace(tzinfo=timezone.utc).timestamp())
        article_data["summary"] = ""
        article_data["title"] = title
        article_data["category"] = "DOTA 2"
        return article_data