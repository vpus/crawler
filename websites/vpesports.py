import requests

class VPEsports():
    def crawl(self):
        response = requests.get("https://vpesports-falcon.wl.r.appspot.com/news/all?limit=10")
        article_data_list = response.json()["data"]
        for article in article_data_list:
            article["is_original"] = True
        return article_data_list