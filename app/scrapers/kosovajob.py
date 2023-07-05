from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
import requests
import logging
from app.models.kosovajob import Job
from app.utils.database import session



class KosovajobScraper(Scraper):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def scrape(self, url_path: str):
        results = []
        response = requests.get(url_path)
        soup = BeautifulSoup(response.content, "html.parser")

        parent_divs = soup.find_all('div', class_='jobListCntsInner')
        for parent_div in parent_divs:
            job_title = parent_div.find('div', class_='jobListTitle').text
            city = parent_div.find('div', class_='jobListCity').text
            expire_date = parent_div.find('div', class_='jobListExpires').text
            results.append({'title': job_title, 'city': city, 'expire_date': expire_date})

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
                title=result['title'],
                city=result['city'],
                expire_date=result['expire_date']
            )
            session.add(job)

        session.commit()
