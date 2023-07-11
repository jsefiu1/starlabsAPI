from app.scrapers.base import Scraper
from app.utils.database import session
from app.models.douglas import Brand
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import logging
import re

class DouglasScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)      
    def scrape(self, url_path: str, page_numbers: int):
        scrape_url = f"{self.base_url}{url_path}"
        results = []
        for page in range(1, page_numbers + 1):
            scrape_url = f"{self.base_url}/c/{url_path}/?page={page}"
            html_text = requests.get(scrape_url).text
            soup = BeautifulSoup(html_text, "lxml")
            item_elements = soup.find_all("div", class_="product-grid-column col-sm-6 col-md-4 col-lg-3")
            #print(scrape_url)
            #print(html_text)

                
            for item in item_elements:
                name = item.find("div", class_="text top-brand").text.strip().replace("ô", "o")
                category = item.find("div", class_="text category").text.strip()

                price_offer = item.find("div", class_=["price-row"])
                price_offer = price_offer.text.strip() if price_offer is not None else None
                    #price_offer = re.sub(r"[^\d.]", "", price_offer)

                    

                price = item.find("div", class_=["product-price__strikethrough product-price__strikethrough--unit price-row__price price-row__price--original-price"])
                price = price.text.strip().replace("UVP", "") if price is not None else None
                    #price = re.sub(r"[^\d.]", "", price)

                    
                details_link = item.find("a", "link link--no-decoration product-tile__main-link").get('href')
                date_scraped = datetime.now()
                if details_link is not None:
                    details_link = "https://www.douglas.de" + details_link
                results.append({"name": name, "category": category, "price": price or price_offer or None, "details_link": details_link, "date_scraped":date_scraped})
                
        return results
    
    def save_to_db( results):
        try:
            for result in results:
                existing_brand = session.query(Brand).filter_by(details_link=result["details_link"]).first()
                if existing_brand is None:
                    brands = Brand(
                        name=result["name"],
                        category=result["category"],
                        price=result["price"],
                        details_link=result["details_link"],
                        date_scraped=result["date_scraped"],
                    )
                    session.add(brands)
            session.commit()
        except Exception as e:
            logging.error(f"Error saving to database.")