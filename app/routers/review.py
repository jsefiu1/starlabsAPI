from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.models.review import Review
from app.utils.database import SessionLocal

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/review", response_class=HTMLResponse)
def reviews_list(request: Request):
    db = SessionLocal()
    review = db.query(Review).all()
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    return templates.TemplateResponse(
        "review.html", {"request": request, "review": review, "username": username, "user_role": user_role}
    )

@router.post("/submit-review", response_class=RedirectResponse)
def submit_review(request: Request, reviewTitle: str = Form(...), reviewContent: str = Form(...), user: Register = Depends(manager)):
    db = SessionLocal()
    new_review = Review(title=reviewTitle, content=reviewContent, author=user.username)
    db.add(new_review)
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)