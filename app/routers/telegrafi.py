from fastapi import APIRouter, Request
from app.models.telegrafi import Article
from app.scrapers.telegrafi import TelegrafiScraper
from app.utils.database import session
from datetime import datetime, timedelta
from sqlalchemy import func
from fastapi.templating import Jinja2Templates
from math import ceil

router = APIRouter(prefix="/telegrafi")
templates = Jinja2Templates(directory="app/templates")
limit = 10


@router.post("/scrape")
async def scrape_telegrafi(url_path: str, page_numbers: int, get_details: bool = False):
    telegrafi_scraper = TelegrafiScraper(base_url="https://telegrafi.com")
    results = telegrafi_scraper.scrape(
        url_path=url_path, page_numbers=page_numbers, get_details=get_details
    )
    TelegrafiScraper.insert_to_DB(results=results)
    return results


@router.get("/data")
async def telegrafi_data(
    article_id: int = None,
    title_contains: str = None,
    date_from: str = None,
    date_to: str = None,
    offset: int = None,
    limit: int = None,
):
    articles = session.query(Article)

    if article_id:
        articles = articles.filter(Article.id == article_id)

    if title_contains:
        articles = articles.filter(Article.name.ilike(f"%{title_contains}%"))

    if date_from:
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            articles = articles.filter(Article.date_posted >= date_from)
        except ValueError:
            return {"error": "Invalid date format. Please use YYYY-MM-DD."}
    if date_to:
        try:
            date_to = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
            articles = articles.filter(Article.date_posted < date_to)
        except ValueError:
            return {"error": "Invalid date format. Please use YYYY-MM-DD."}

    total_articles = articles.count()
    if total_articles > 0:
        if limit:
            total_pages = int(ceil(total_articles / limit))
        else:
            total_pages = int(ceil(total_articles / total_articles))
    else:
        total_pages = 1

    articles = articles.offset(offset).limit(limit)
    results = []
    for article in articles:
        results.append(article.__dict__)

    return {"results": results, "total_pages": total_pages}


@router.get("/view")
async def telegrafi_view(
    request: Request,
    title_contains: str = None,
    date_from: str = None,
    date_to: str = None,
    page: int = 1,
):
    offset = (page - 1) * limit
    result = await telegrafi_data(
        title_contains=title_contains,
        date_from=date_from,
        date_to=date_to,
        offset=offset,
        limit=limit,
    )
    results = result["results"]
    total_pages = result["total_pages"]

    return templates.TemplateResponse(
        "telegrafi.html",
        {
            "request": request,
            "results": results,
            "current_page": page,
            "total_pages": total_pages,
            "title_contains": title_contains,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
