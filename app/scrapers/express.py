from datetime import datetime
import logging
from app.models.express import Lajme
from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
import requests
from app.utils.database import session

class ExpressScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def scrape(self, url_path: str, limit: int, offset: int):
        results = []
        scrape_url = f"{self.base_url}/{url_path}/"
        html_text = requests.get(scrape_url).text
        soup = BeautifulSoup(html_text, "lxml")
        container = soup.find("body")

        lajmet = container.find_all("a", class_="col-6")

        for i, lajme in enumerate(lajmet[offset : offset + limit]):
            name = lajme.find("h3", class_="box__title").text.strip()
            name2 = lajme.find("h3", class_="box__title").text.strip().replace("ë", "e").replace("ç", "c")
            details = lajme.get("href")
            image_item = lajme.find("img")
            image_link = image_item.get("src") if image_item else "No link found"
            date_scraped = datetime.now()
            data = {
                "id": i + offset + 1,
                "name": name,
                "name2": name2,
                "details": details,
                "image_link": image_link,
                "date_scraped": date_scraped,
            }
            results.append(data)

        return results
    
    def insert_to_DB(results):
        try:
            for result in results:
                existing_item = session.query(Lajme).filter_by(details=result["details"]).first()
                if existing_item:
                    continue

                lajme = Lajme(
                    name=result["name"],
                    name2=result["name2"],
                    details=result["details"],
                    image=result["image_link"],
                    date_scraped=result["date_scraped"],
                )

                session.add(lajme)
                session.commit()
        except Exception as e:
            logging.error(f"Error in saving data to the database: {e}")

