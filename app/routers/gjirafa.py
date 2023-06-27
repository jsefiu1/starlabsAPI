from fastapi import APIRouter, Query
from app.models.gjirafa import Product
from app.scrapers.gjirafa import GjirafaScraper
from app.utils.database import session
from decimal import Decimal 

router = APIRouter(prefix="/gjirafa")

@router.get("/scrape")
async def gjirafa_scrape(url_path: str = Query(default="headphones"), page_numbers: int = Query(default=1)):
    gjirafa_scraper = GjirafaScraper(base_url="https://gjirafamall.com/search?q=")
    results = gjirafa_scraper.scrape(url_path=url_path,page_numbers=page_numbers)

    gjirafa_scraper.save_to_db(results)

    return results


@router.get("/data")
async def gjirafa_data():
    products = session.query(Product)
    results = []
    for product in products:
        results.append(product.__dict__)
    return results

    # def save_to_db(self, results):
    #     for result in results:
    #         product = Product(
    #             name=result["name"],
    #             price=result["price"],
    #             details_link=result["details_link"],
    #     )
        
        # session.add(product)
        # session.commit()

    # return results