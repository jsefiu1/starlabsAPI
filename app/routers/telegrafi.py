from fastapi import APIRouter
from app.models.telegrafi import Article
from app.scrapers.telegrafi import TelegrafiScraper
from app.utils.database import session

router = APIRouter(prefix="/telegrafi")


@router.get("/scrape")
async def scrape_telegrafi(url_path: str, page_numbers: int):
    telegrafi_scraper = TelegrafiScraper(base_url="https://telegrafi.com")
    results = telegrafi_scraper.scrape(url_path=url_path, page_numbers=page_numbers)

    for result in results:
        article = Article(
            name=result["name"],
            details_link=result["details_link"],
            image_link=result["image_link"],
            date_posted=result["date_posted"],
        )

        session.add(article)
        session.commit()

    return results


@router.get("/data")
async def telegrafi_data():
    articles = session.query(Article)
    results = []
    for article in articles:
        results.append(article.__dict__)
    return results
