from app.scrapers.base import Scraper
from bs4 import BeautifulSoup
import requests
import logging
from app.models.kosovajob import Job
from app.utils.database import session
from datetime import datetime


class KosovajobScraper(Scraper):
    def init(self, base_url: str):
        super().__init__(base_url)

    def scrape(self):
        current_date = datetime.now()
        date_of_scrape = current_date.strftime("%d/%m/%Y %H:%M")
        results = []
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, "html.parser")

        parent_divs = soup.find_all("div", class_="jobListCnts")
        for parent_div in parent_divs:
            image_div = parent_div.find("div", class_="jobListImage")
            image_url = image_div["data-background-image"]
            job_title = parent_div.find("div", class_="jobListTitle").text
            city_element = parent_div.find("div", class_="jobListCity")
            city = city_element.text.strip() if city_element else None
            expires_date = parent_div.find("div", class_="jobListExpires").text
            details_link = parent_div.find("a")["href"]
            results.append(
                {
                    "image_url": image_url,
                    "title": job_title,
                    "city": city,
                    "details_link": details_link,
                    "expires_date": expires_date,
                    "date_of_scrape": date_of_scrape,
                }
            )

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
                image_url=result["image_url"],
                title=result["title"],
                city=result["city"],
                expires_date=result["expires_date"],
                details_link=result["details_link"],
                date_of_scrape=result["date_of_scrape"],
            )
            if session.query(Job).filter_by(title=job.title).first():
                continue
            session.add(job)

        session.commit()
