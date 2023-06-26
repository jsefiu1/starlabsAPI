from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
import requests

class GjirafaScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)
 
    def scrape(self, url_path: str):
        scrape_url = f"{self.base_url}{url_path}"
        results = []
        page = 1

        while True:
            page_url = f"{scrape_url}&i={page}"
            html_text = requests.get(page_url).text
            soup = BeautifulSoup(html_text, "html.parser")
            product_elements = soup.find_all("div", class_="art-inner")
            
            if not product_elements:
                break

            for product in product_elements:
                name = product.find("span", class_="px-3 text-center").text.strip()
                try:
                    price = product.find("span", class_="ml-3 mr-2 art-price").text.strip()
                except AttributeError:
                    price = None
                try:
                    price_offer = product.find("span", class_="ml-3 mr-2 art-price art-price--offer").text.strip()
                except AttributeError:
                    price_offer = None

                results.append({"name": name, "price": price or price_offer or None})

            page += 1

        return results


# class GjirafaScraper(Scraper):
#     def __init__(self, base_url: str):
#         super().__init__(base_url)

#     def scrape(self, url_path: str):
#         scrape_url = f"{self.base_url}{url_path}"
#         html_text = requests.get(scrape_url).text
#         soup = BeautifulSoup(html_text, "html.parser")
#         product_elements = soup.find_all("div", class_="art-inner")
#         results = []
#         for product in product_elements:
#             name = product.find("span", class_="px-3 text-center").text.strip()
#             try:
#                 price = product.find("span", class_="ml-3 mr-2 art-price").text.strip()
#             except AttributeError:
#                 price = None
#             try:
#                 price_offer = product.find("span", class_="ml-3 mr-2 art-price art-price--offer").text.strip()
#             except AttributeError:
#                 price_offer = None

#             results.append({"name": name, "price": price or price_offer or None})

#         return results
