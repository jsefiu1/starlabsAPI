from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.database import session
from app.models.ofertasuksesi import Data
from app.scrapers.ofertasuksesi import scrape
from typing import Optional
from math import ceil

router = APIRouter(tags=["ofertasukesi"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/ofertasuksesi/html", response_class=HTMLResponse)
def get_ofertasuksesi_html(request: Request, page: Optional[int] = Query(1, ge=1), current_page: Optional[int] = Query(default=1, ge=1)):
    items_per_page = 10
    offers = session.query(Data).all()
    total_items = len(offers)
    total_pages = ceil(total_items / items_per_page)

    if not offers:
        raise HTTPException(status_code=404, detail="No data in database")

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_offers = offers[start_index:end_index]

    template = templates.get_template("ofertasuksesi.html")
    rendered_html = template.render(offers=current_offers, current_page=page, pagination_numbers=range(1, total_pages + 1), total_pages=total_pages)

    return rendered_html

@router.get("/search", response_class=HTMLResponse)
def search_offers(query: Optional[str], request: Request, page: Optional[int] = Query(1, ge=1), current_page: Optional[int] = Query(default=1, ge=1)):
    format_query = query.title()
    items_per_page = 10
    check_offers = session.query(Data).filter(Data.location.contains(format_query)).all()
    total_items = len(check_offers)
    total_pages = ceil(total_items / items_per_page)

    if not check_offers:
        raise HTTPException(status_code=404, detail="No data in database")

    if query:
        items_per_page = total_items

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_offers = check_offers[start_index:end_index]

    template = templates.get_template("ofertasuksesi.html")
    rendered_html = template.render(offers=current_offers, current_page=page, pagination_numbers=range(1, total_pages + 1), total_pages=total_pages)

    return rendered_html

@router.get("/ofertasuksesi/scrape")
def offertasuksesi_data(category: str, page: int):
    return scrape(category=category, page=page)

@router.get("/ofertasuksesi/data")
def get_ofertasuksesi_data():
    offers = session.query(Data).all()
    if not offers:
        raise HTTPException(status_code=404, detail="No data in database")
    else:
        return offers
    
@router.get("/ofertasuksesi/by-title-location")
def get_ofertasuksesi_by_title_location(title: str = Query(None), location: str = Query(None)):
    format_loc = location.title().replace(" ", "")
    offer = session.query(Data).filter(Data.title == title, Data.location == format_loc).first()
    if offer is None:
        raise HTTPException(status_code=404, detail="Title or location not found")
    else:
        return offer