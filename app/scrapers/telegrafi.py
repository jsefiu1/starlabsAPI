from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import logging
from app.utils.time import string_ago_to_datetime
from app.models.telegrafi import Article
from app.utils.database import session


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
                date_scraped = datetime.now()
                data = {
                    "name": name,
                    "details_link": details_link,
                    "image_link": image_link,
                    "date_posted": date_posted,
                    "date_scraped": date_scraped,
                }

                results.append(data)
        return results

    def insert_to_DB(results):
        try:
            for result in results:
                article = Article(
                    name=result["name"],
                    details_link=result["details_link"],
                    image_link=result["image_link"],
                    date_posted=result["date_posted"],
                    date_scraped=result["date_scraped"],
                )

                if session.query(Article).filter_by(name=article.name).first():
                    continue

                session.add(article)
                session.commit()
        except Exception as e:
            logging.error(f"Error in saving data to the database: {e}")
