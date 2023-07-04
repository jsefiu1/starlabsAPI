from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
import requests
import logging
from app.models.kosovajob import Job
from app.utils.database import session
from datetime import date


class KosovajobScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def scrape(self, url_path: str):
        current_date = date.today()
        date_of_scrape = current_date.strftime("%d/%m/%Y")
        results = []
        response = requests.get(url_path)
        soup = BeautifulSoup(response.content, "html.parser")

        parent_divs = soup.find_all('div', class_='jobListCnts')
        for parent_div in parent_divs:
            image_div = parent_div.find('div', class_='jobListImage')
            image_url = image_div['data-background-image']
            job_title = parent_div.find('div', class_='jobListTitle').text
            city = parent_div.find('div', class_='jobListCity').text
            expires_date = parent_div.find('div', class_='jobListExpires').text
            results.append({'image_url': image_url,'title': job_title, 'city': city, 'expires_date': expires_date, 'date_of_scrape': date_of_scrape})

        if results:
            return results
        else:
            print("No results found.")
            return []

    def save_to_db(self, results, session):
        if not results:
            return

        for result in results:
            job = Job(
                image_url=result['image_url'],
                title=result['title'],
                city=result['city'],
                expires_date=result['expires_date'],
                date_of_scrape=result['date_of_scrape']
            )
            session.add(job)

        session.commit()
