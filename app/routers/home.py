from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/home")

@router.get("/home")
async def home(request: Request):
    navigation_items = [
        {"name": "Dashboard", "url": "/home"},
        {"name": "Telegrafi", "url": "/telegrafi/view"},
        {"name": "Gjirafa", "url": "/gjirafa/view"},
        {"name": "Douglas", "url": "/douglas/view"},
        {"name": "Kosovajobs", "url": "/kosovajobs/view"}
        # Add more navigation items as needed
    ]
    return templates.TemplateResponse(
        "home.html", {"request": request, "navigation_items": navigation_items}
    )
