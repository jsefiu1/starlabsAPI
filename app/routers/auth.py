from fastapi import APIRouter, FastAPI, Depends, HTTPException, Form, Request, status
from fastapi.responses import FileResponse, Response, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from app.utils.database import session, SessionLocal
from app.models.auth import Register
from datetime import datetime, timedelta

SECRET_KEY = "78a061b526f62f90728cc54090af38cfa8c0228cc81aa2a2"
ACCESS_TOKEN_EXPIRES_MINUTES = 60
manager = LoginManager(secret=SECRET_KEY, token_url="/login", use_cookie=True)
manager.cookie_name = "auth"

@manager.user_loader()
def get_user_from_db(username: str):
    db = SessionLocal()
    user = db.query(Register.username == username).first()
    return user

def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(Register).filter(Register.username == username).first()
    if not user:
        return None
    
    if not verify_password(plain_password=password, hashed_password=user.password):
        return None
    
    return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# router = APIRouter(tags=["User Data"])
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

class NotAuthenticatedException(Exception):
    pass

def not_authenticated_exception_handler(request, exception):
    return RedirectResponse(url="/login")

# manager.not_authenticated_handler = NotAuthenticatedException
manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)

@app.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "invalid": True}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = manager.create_access_token(data={"sub": user.username}, expires=access_token_expires)
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.get("/register", response_class=HTMLResponse)
def register_html(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    hashed_password = get_hashed_password(password)
    new_user = Register(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=302)


@app.get("/data")
def data(request: Request, user: Register = Depends(manager)):
    navigation_items = [
        {"name": "Dashboard", "url": "/data"},
        {"name": "Telegrafi", "url": "/telegrafi/view"},
        {"name": "Gjirafa", "url": "/gjirafa/view"},
        {"name": "ofertasuksesi", "url": "/ofertasuksesi/html"},
        {"name": "Douglas", "url": "/douglas/view"},
        {"name": "Kosovajobs", "url": "/kosovajobs/view"},
        {"name": "Express", "url": "/gazetaexpress/view"}
        # Add more navigation items as needed
    ]
    return templates.TemplateResponse(
        "data.html", {"request": request, "navigation_items": navigation_items, "user": user}
    )
        
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/logout")
def logout():
    response = RedirectResponse("/login")
    manager.set_cookie(response, None)
    return response

# app.include_router(router)