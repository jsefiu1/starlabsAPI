from fastapi import APIRouter
from app.models.scrapers import Product
from app.scrapers.base import Gjirafa50Scraper
from app.utils.database import session

router = APIRouter(prefix="/gjirafa50")


@router.get("")
async def gjirafa50_test():
    gjirafa_scraper = Gjirafa50Scraper(base_url="https://gjirafa50.com")
    results = gjirafa_scraper.scrape(url_path="")

    for result in results:
        product = Product(
            name=result["name"],
            price=result["price"],
            details_link=result["details_link"],
            discount_price=result["discount_price"],
            image_link=result["image_link"],
            is_risi=result["is_risi"],
            is_24h=result["is_24h"],
        )

        session.add(product)
        session.commit()

    return results
