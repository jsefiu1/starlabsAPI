from fastapi import APIRouter, Query
from app.models.gjirafa import Product
from app.scrapers.gjirafa import GjirafaScraper
from app.utils.database import session

router = APIRouter(prefix="/gjirafa")

@router.get("/scrape")
async def gjirafa_scrape(url_path: str = Query(default="headphones")):
    base_url = "https://gjirafamall.com/search?q="
    gjirafa_scraper = GjirafaScraper(base_url=base_url)
    results = gjirafa_scraper.scrape(url_path=url_path)

    for result in results:
        product = Product(
            name=result["name"],
            price=result["price"],
        )

        session.add(product)
        session.commit()

    return results
