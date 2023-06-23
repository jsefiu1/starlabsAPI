from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
import requests


class TelegrafiScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def scrape(self, url_path: str):
        scrape_url = f"{self.base_url}{url_path}"
        html_text = requests.get(scrape_url).text
        soup = BeautifulSoup(html_text, "lxml")
        articles = soup.find(
            "div", class_="catgory-latest category-page--listing"
        ).find_all("a")
        results = []
        for article in articles:
            name = article.get("data-vr-contentbox")
            if name is None:
                continue
            details_link = article.get("href")
            image_item = article.find("img")
            image_link = image_item.get("src") if image_item else "No link found"
            results.append(
                {"name": name, "details_link": details_link, "image_link": image_link}
            )

        return results
