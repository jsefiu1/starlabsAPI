from fastapi import APIRouter, Query
from app.models.douglas import Brand
from app.scrapers.douglas import DouglasScraper
from app.utils.database import session

router = APIRouter(prefix="/douglas")


@router.get("/scrape")
def douglas_scrape(url_path: str, page_numbers: int):
    douglas_scraper = DouglasScraper(base_url="https://www.douglas.de/en")
    results = douglas_scraper.scrape(url_path=url_path, page_numbers=page_numbers)
    DouglasScraper.save_to_db(results=results)
    return results

@router.get("/data")
def douglas_data():
    brands = session.query(Brand)
    results = []
    for brand in brands:
        results.append(brand.__dict__)
    return results