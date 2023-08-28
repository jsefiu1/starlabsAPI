from app.models.auth import Contact
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
router = APIRouter()

@router.post("/submit_contact_form")
async def submit_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    contact_entry = Contact(name=name, email=email, message=message)
    db.add(contact_entry)
    db.commit()
    
    return {"message": "Thank you for your message!"}


