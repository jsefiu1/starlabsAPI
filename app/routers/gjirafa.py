from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from app.models.gjirafa import Product
from app.scrapers.gjirafa import GjirafaScraper
from app.utils.database import session
from math import ceil
from decimal import Decimal

router = APIRouter(prefix="/gjirafa")
templates = Jinja2Templates(directory="app/templates")
limit = 10

@router.get("/scrape")
async def gjirafa_scrape(url_path: str = Query(default="Sport"), page_numbers: int = Query(default=1)):
    gjirafa_scraper = GjirafaScraper(base_url="https://gjirafamall.com/")
    results = gjirafa_scraper.scrape(url_path=url_path, page_numbers=page_numbers)

    gjirafa_scraper.save_to_db(results)
    return results


@router.get("/data")
async def gjirafa_data(
    request: Request,
    title_contains: str = None,
    offset: int = None,
    limit: int = None,
    limit_price: float = None,
):
    products = session.query(Product)

    if title_contains:
        products = products.filter(Product.name.ilike(f"%{title_contains}%"))

    if limit_price is not None:  # Check if limit_price is not None
        products = products.filter(Product.price < limit_price)

    total_products = products.count()
    if total_products > 0:
        if limit:
            total_pages = int(ceil(total_products / limit))
        else:
            total_pages = 1
    else:
        total_pages = 1

    products = products.offset(offset).limit(limit)
    results = [product.__dict__ for product in products]

    return {"results": results, "total_pages": total_pages}

@router.get("/view")
async def gjirafa_view(request: Request, title_contains: str = None,
    limit_price: str = None,  # Change the type to string
    page: int = 1,
):
    offset = (page - 1) * limit

    if limit_price and limit_price.strip() != "":
        limit_price = float(limit_price)
    else:
        limit_price = None

    result = await gjirafa_data(
        request=request,
        title_contains=title_contains,
        offset=offset,
        limit=limit,
        limit_price=limit_price,
    )
    results = result['results']
    total_pages = result["total_pages"]

    return templates.TemplateResponse(
        "gjirafa.html",
        {
            "request": request,
            "results": results,
            "current_page": page,
            "total_pages": total_pages,
            "title_contains": title_contains,
            "limit_price": limit_price,
        },
    )
