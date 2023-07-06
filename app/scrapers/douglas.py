from app.scrapers.base import Scraper
from app.utils.database import session
from app.models.douglas import Brand
from bs4 import BeautifulSoup
import requests
import logging

class DouglasScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)      
    def scrape(self, url_path: str, page_numbers: int):
        scrape_url = f"{self.base_url}{url_path}"
        results = []
        for page in range(1, page_numbers + 1):
            scrape_url = f"{self.base_url}/c/{url_path}03/?page={page}"
            html_text = requests.get(scrape_url).text
            soup = BeautifulSoup(html_text, "lxml")
            item_elements = soup.find_all("div", class_="product-grid-column col-sm-6 col-md-4 col-lg-3")
            #print(scrape_url)
            #print(html_text)
            #print(soupprettifyed)
                
            for item in item_elements:
                name = item.find("div", class_="text top-brand").text.strip()
                category = item.find("div", class_="text category").text.strip()
                price = item.find("div", class_="price-row").text.strip()            
                details_link = item.find("a", "link link--no-decoration product-tile__main-link").get('href')
                if details_link is not None:
                    details_link = "https://www.douglas.de/en" + details_link
                    
                results.append({"name": name, "category": category, "price": price or None, "details_link": details_link})
                
        return results
    
    def save_to_db( results):
        try:
            for result in results:
                brands = Brand(
                    name=result["name"],
                    category=result["category"],
                    price=result["price"],
                    details_link=result["details_link"],
                )
                session.add(brands)
            session.commit()
        except Exception as e:
            logging.error(f"Error saving to database.")