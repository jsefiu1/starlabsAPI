from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi import Query
from app.models.models import Product
from app.scrapers.gjirafa import GjirafaScraper
from app.utils.database import session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/gjirafa/scrape")
async def gjirafa_scrape(url_path: str = Query(default="headphones"), page_numbers: int = Query(default=1)):
    gjirafa_scraper = GjirafaScraper(base_url="https://gjirafamall.com/search?q=")
    results = gjirafa_scraper.scrape(url_path=url_path, page_numbers=page_numbers)
    gjirafa_scraper.save_to_db(results)
    return results

@router.get("/gjirafa/data")
async def gjirafa_data(request: Request):
    products = session.query(Product)
    results = []
    for product in products:
        results.append(product.__dict__)
    return templates.TemplateResponse("gjirafa_data.html", {"request": request, "results": results})
