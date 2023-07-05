from app.scrapers.base import Scraper
from app.utils.database import session
from datetime import datetime, timedelta
from app.utils.time import string_ago_to_datetime
from app.models.gjirafa import Product
from bs4 import BeautifulSoup
import re
import requests
import logging

class GjirafaScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        
    def scrape(self, url_path: str, page_numbers: int):
        results = []
        for number in range(1, 6):
            scrape_url = f"{self.base_url}{url_path}-{number}?i="
            
            for page_nr in range(1, page_numbers + 1):
                current_url = f"{scrape_url}{page_nr}"
                html_text = requests.get(current_url).text
                soup = BeautifulSoup(html_text, "html.parser")
                product_elements = soup.find_all("div", class_="art-inner")
                
                if not product_elements:
                    break
                
                for product in product_elements:
                    name = product.find("span", class_="px-3 text-center").text.strip()
                    try:
                        price = product.find("span", class_="ml-3 mr-2 art-price").text.strip()
                        price = re.sub(r"[^\d.]", "", price) 
                        price = float(price) if price else None  
                    except AttributeError:
                        price = None
                    try:
                        price_offer = product.find("span", class_="ml-3 mr-2 art-price art-price--offer").text.strip()
                        price_offer = re.sub(r"[^\d.]", "", price_offer)
                        price_offer = float(price_offer) if price_offer else None 
                    except AttributeError:
                        price_offer = None
                    
                    details_link = product.find("a", class_="art-picture img-center-container").get('href') if product.find("a", class_="art-picture img-center-container") else None
                    if details_link is not None:
                        details_link = "https://gjirafamall.com" + details_link
                    date_scraped = datetime.now()

                    results.append({"name": name, "price": price or price_offer or None, "details_link": details_link, "date_scraped": date_scraped})

        self.save_to_db(results)
        return results
    
    def save_to_db(self, results):
        try:
            for result in results:
                product = Product(
                    name=result["name"],
                    price=result["price"],
                    details_link=result["details_link"],
                    date_scraped=result["date_scraped"],
                )

                if session.query(Product).filter_by(name=product.name).first():
                    continue
                session.add(product)
                session.commit()
        except Exception as e:
            logging.error(f"Error in saving data to the database: {e}")