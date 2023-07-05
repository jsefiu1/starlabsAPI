from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/home")
async def home(request: Request):
    navigation_items = [
        {"name": "Dashboard", "url": "/home"},
        {"name": "Telegrafi", "url": "/telegrafi/view"},
        # Add more navigation items as needed
    ]
    return templates.TemplateResponse(
        "home.html", {"request": request, "navigation_items": navigation_items}
    )
