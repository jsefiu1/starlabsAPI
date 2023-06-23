from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def scrape(self, url_path: str):
        raise NotImplementedError


class Gjirafa50Scraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def scrape(self, url_path: str):
        scrape_url = f"{self.base_url}{url_path}"
        html_text = requests.get(scrape_url).text
        soup = BeautifulSoup(html_text, "lxml")
        products = soup.find_all("div", class_="item-box")
        results = []
        for product in products:

            name = "Spe dina"
            price = product.find("span", class_="price")
            details_link = "spe dina 2"
            discount_price = None  # TODO: implement this
            image_link = product.find("div", class_="picture").find("a")["href"]
            is_risi = False  # TODO: implement this
            is_24h = False  # TODO: implement this

            results.append(
                {
                    "name": name,
                    "price": price,
                    "details_link": details_link,
                    "discount_price": discount_price,
                    "image_link": image_link,
                    "is_risi": is_risi,
                    "is_24h": is_24h,
                }
            )

        return results
