from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
import requests
from app.utils.time import string_ago_to_datetime


class TelegrafiScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def scrape(self, url_path: str, page_numbers: int):
        results = []
        for page_nr in range(1, page_numbers + 1):
            scrape_url = f"{self.base_url}{url_path}page/{page_nr}/"
            html_text = requests.get(scrape_url).text
            soup = BeautifulSoup(html_text, "lxml")
            main_div = soup.find(
                "div", {"class": "catgory-latest category-page--listing"}
            )

            mobile_elements = main_div.find_all(class_="mobileAgent")

            for element in mobile_elements:
                element.extract()

            articles = main_div.find_all("a", class_="post__large")

            for article in articles:

                name = article.get("data-vr-contentbox")
                if name is None:
                    continue
                details_link = article.get("href")
                image_item = article.find("img")
                image_link = image_item.get("src") if image_item else "No link found"
                time_ago = article.find("div", class_="post_date_info").text
                date_posted = string_ago_to_datetime(time_ago)
                data = {
                    "name": name,
                    "details_link": details_link,
                    "image_link": image_link,
                    "date_posted": date_posted,
                }

                results.append(data)
        return results
