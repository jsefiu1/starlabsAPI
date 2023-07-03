from fastapi import APIRouter, Request,Query
from sqlalchemy import func
from app.utils.database import session
from app.models.kosovajob import Job
from app.scrapers.kosovajob import KosovajobScraper


router=APIRouter(
    prefix='/kosovajobs',
)


@router.get('/scrape')
def scrape_and_insert(url_path: str):
    kosovajob_scraper=KosovajobScraper(base_url='https://kosovajob.com/')
    results = kosovajob_scraper.scrape(url_path=url_path)
    kosovajob_scraper.save_to_db(results=results,session=session)
    return results

@router.get('/data')
def get_data(title: str = Query(None),city: str = Query(None)):
    if title:
        jobs = session.query(Job).filter(func.lower(Job.title).contains(title.lower())).all()
    if city:
        jobs = session.query(Job).filter(func.lower(Job.city).contains(city.lower())).all()
    if not title and not city:
        jobs = session.query(Job).all()
    return jobs

