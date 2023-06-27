from fastapi import APIRouter
from app.models.telegrafi import Article
from app.scrapers.telegrafi import TelegrafiScraper
from app.utils.database import session
from datetime import datetime, timedelta
from sqlalchemy import func


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
async def telegrafi_data(
    title_contains: str = None, date_from: str = None, date_to: str = None
):
    articles = session.query(Article)

    if title_contains:
        articles = articles.filter(
            func.lower(Article.name).like(func.lower(f"%{title_contains}%"))
        )

    if date_from and date_to:
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
            articles = articles.filter(Article.date_posted.between(date_from, date_to))
        except ValueError:
            return {"error": "Invalid date format. Please use YYYY-MM-DD."}

    results = []
    for article in articles:
        results.append(article.__dict__)
    return results
