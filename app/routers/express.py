from fastapi import APIRouter
from app.models.express import Lajme
from app.scrapers.express import ExpressScraper
from app.utils.database import session
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from math import ceil
from sqlalchemy.sql.expression import bindparam
from typing import Optional





templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/gazetaexpress")
limit = 10


@router.get("/scrape")
async def scrape_express(url_path: str, limit: int, offset: int = 0): 

    express_scraper = ExpressScraper(base_url="https://www.gazetaexpress.com")
    results = express_scraper.scrape(url_path=url_path, limit=limit, offset=offset)
    ExpressScraper.insert_to_DB(results)

    return results

@router.get("/data")
async def express_data(
    title_contains: str = None,
    offset: int = None,
    limit: int = None,
):
    
    lajme = session.query(Lajme)

    if title_contains:
        lajme = lajme.filter(
        (Lajme.name.ilike(f"%{title_contains}%")) | (Lajme.name2.ilike(f"%{title_contains}%"))
    )

    total_lajme = lajme.count()
    if total_lajme > 0:
        if limit:
            total_pages = int(ceil(total_lajme / limit))
        else:
            total_pages = int(ceil(total_lajme / total_lajme))
    else:
        total_pages = 1

    lajme = lajme.offset(offset).limit(limit)
    results = []
    for lajme in lajme:
        results.append(lajme.__dict__)

    return {"results": results, "total_pages": total_pages}


@router.get("/view")
async def view(request: Request, page: int = 1, title_contains: str=None,):
    offset = (page - 1) * limit
    result = await express_data(
        title_contains = title_contains,
        offset=offset,
        limit=limit,
    )
    results = result["results"]
    total_pages = result["total_pages"]

    return templates.TemplateResponse(
        "express.html",
        {
            "request": request,
            "results": results,
            "total_pages": total_pages,
            "title_contains": title_contains,
            "current_page": page,
        },
    )
