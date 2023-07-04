from fastapi import APIRouter, Request,Query
from sqlalchemy import func
from app.utils.database import session
from app.models.kosovajob import Job
from app.scrapers.kosovajob import KosovajobScraper
import requests
from fastapi.templating import Jinja2Templates
from typing import Optional
from math import ceil
router=APIRouter(
    prefix='/kosovajobs',)
templates = Jinja2Templates(directory="app/templates")


@router.get('/scrape')
def scrape_and_insert(url_path: str):
    kosovajob_scraper=KosovajobScraper(base_url='https://kosovajob.com/')
    results = kosovajob_scraper.scrape(url_path=url_path)
    kosovajob_scraper.save_to_db(results=results,session=session)
    return results

@router.get('/data')
def kosovajob_data(title: str = Query(None),city: str = Query(None)):
    if title and city:
        jobs = session.query(Job).filter(func.lower(Job.title).contains(title.lower()), func.lower(Job.city).contains(city.lower())).all()
    elif title:
        jobs = session.query(Job).filter(func.lower(Job.title).contains(title.lower())).all()
    elif city:
        jobs = session.query(Job).filter(func.lower(Job.city).contains(city.lower())).all()
    else:
        jobs = session.query(Job).all()
    return jobs


@router.get('/view')
def dashboard(
    request: Request,
    jobtitle: Optional[str] ='',
    city: Optional[str] = '',
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1, le=100), 
):
    query = session.query(Job)
    if jobtitle and city:
        query = query.filter(func.lower(Job.title).contains(jobtitle.lower()), func.lower(Job.city).contains(city.lower()))
    elif jobtitle:
        query = query.filter(func.lower(Job.title).contains(jobtitle.lower()))
    elif city:
        query = query.filter(func.lower(Job.city).contains(city.lower()))

    
    total_jobs = query.count()
    total_pages = ceil(total_jobs / page_size)

    max_visible_pages = 5
    buffer_pages = max_visible_pages - 2

    if total_pages <= max_visible_pages:
        start_page = 1
        end_page = total_pages
    else:
        if page <= buffer_pages:
            start_page = 1
            end_page = max_visible_pages - 1
        elif page > total_pages - buffer_pages:
            start_page = total_pages - max_visible_pages + 2
            end_page = total_pages
        else:
            start_page = page - (buffer_pages // 2)
            end_page = page + (buffer_pages // 2)

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    jobs = query.all()

    return templates.TemplateResponse('kosovajob.html', {
        'request': request,
        'jobs': jobs,
        'jobtitle': jobtitle,
        'city': city,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'start_page': start_page,
        'end_page': end_page,
    })











