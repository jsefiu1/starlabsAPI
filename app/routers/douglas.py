from fastapi import APIRouter, Request, Query
from app.models.douglas import Brand
from app.scrapers.douglas import DouglasScraper
from app.utils.database import session
from sqlalchemy import func
from fastapi.templating import Jinja2Templates
from math import ceil

router = APIRouter(prefix="/douglas")
templates = Jinja2Templates(directory="app/templates")
limit = 10


@router.post("/scrape")
async def douglas_scrape(url_path: str= Query(default="Make-up/"), page_numbers: int = Query(default=1)):
    douglas_scraper = DouglasScraper(base_url="https://www.douglas.de")
    results = douglas_scraper.scrape(url_path=url_path, page_numbers=page_numbers)
    DouglasScraper.save_to_db(results=results)
    return results

@router.get("/data")
async def douglas_data(
    category_contains: str = None,
    offset: int = None,
    limit: int = None,
    limit_price: float = None
):
    brands = session.query(Brand)
    if category_contains:
        brands = brands.filter(Brand.category.ilike(f"%{category_contains}%"))
    
    if limit_price is not None:
        brands = brands.filter(Brand.price <= limit_price)
        
        
        
    total_brands = brands.count()
    if total_brands > 0:
        if limit:
            total_pages = int(ceil(total_brands / limit))
        else:
            total_pages = int(ceil(total_brands / total_brands))
    else:
        total_pages = 1
        
    
    brands = brands.offset(offset).limit(limit)
    results = []
    for brand in brands:
        results.append(brand.__dict__)
    return {"results": results, "total_pages": total_pages}


@router.get("/view")
async def douglas_view(
    request: Request,
    category_contains: str = None,
    limit_price: str = None,
    page: int = 1,
):
    offset = (page - 1) * limit
    
    if limit_price and limit_price.strip() != "":
        limit_price = float(limit_price)
    else:
         limit_price = None
         
    result = await douglas_data(
        category_contains=category_contains,
        offset=offset,
        limit=limit,
        limit_price=limit_price
    )
    results = result["results"]
    total_pages = result["total_pages"]
    
    return templates.TemplateResponse(
        "douglas.html",
        {
            "request": request,
            "results": results,
            "current_page": page,
            "total_pages": total_pages,
            "category_contains": category_contains,
            "limit_price": limit_price
        },
    )