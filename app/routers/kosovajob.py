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


@router.post('/scrape')
def scrape_and_insert(url_path: str):
    kosovajob_scraper=KosovajobScraper(base_url='https://kosovajob.com/')
    results = kosovajob_scraper.scrape(url_path=url_path)
    kosovajob_scraper.save_to_db(results=results,session=session)
    return results

@router.get('/data')
def kosovajob_data(
    title: str = Query(None),
    city: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None)
):
    query = session.query(Job)

    if title and city:
        query = query.filter(
            func.lower(Job.title).contains(title.lower()),
            func.lower(Job.city).contains(city.lower())
        )
    elif title:
        query = query.filter(func.lower(Job.title).contains(title.lower()))
    elif city:
        query = query.filter(func.lower(Job.city).contains(city.lower()))

    total_jobs = query.count()
    if total_jobs > 0:
        if limit:
            total_pages = int(ceil(total_jobs / limit))
        else:
            total_pages = 1
    else:
        total_pages = 0

    if offset is not None:
        query = query.offset(offset * limit)

    if limit is not None:
        query = query.limit(limit)

    results = [job.__dict__ for job in query]

    return {"results": results, "total_pages": total_pages}




@router.get('/view')
def dashboard(
    request: Request,
    jobtitle: Optional[str] ='',
    city: Optional[str] = '',
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1), 
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