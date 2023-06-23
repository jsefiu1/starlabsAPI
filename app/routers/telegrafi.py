from fastapi import APIRouter
from app.models.telegrafi import Article
from app.scrapers.telegrafi import TelegrafiScraper
from app.utils.database import session

router = APIRouter(prefix="/telegrafi")


@router.get("/scrape")
async def telegrafi_test(url_path: str):
    telegrafi_scraper = TelegrafiScraper(base_url="https://telegrafi.com")
    results = telegrafi_scraper.scrape(url_path=url_path)

    for result in results:
        article = Article(
            name=result["name"],
            details_link=result["details_link"],
            image_link=result["image_link"],
        )

        session.add(article)
        session.commit()

    return results
