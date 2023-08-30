from fastapi import APIRouter, Depends, Form, HTTPException, Request
from app.models.auth import Contact
from sqlalchemy.orm import Session
from app.utils.database import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/submit_contact_form")
async def submit_contact_form(
    request: Request, 
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    contact_entry = Contact(name=name, email=email, message=message)
    db.add(contact_entry)
    db.commit()
    

    template_vars = {"name": name, "message": message, "current_page": 1}
    return templates.TemplateResponse("submit_contact_form.html", {"request": request, **template_vars})


