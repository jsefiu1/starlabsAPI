class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def scrape(self, url_path: str):
        raise NotImplementedError
