from fastapi import FastAPI, Depends, Form, Request, status
from fastapi.templating import Jinja2Templates
import uvicorn
from app.routers import telegrafi, gjirafa, kosovajob, express, douglas, ofertasuksesi, home
from app.models import Base
from app.utils.database import engine, SessionLocal, session
from app.tasks import (
    telegrafi as telegrafi_tasks,
    gjirafa as gjirafa_tasks,
    kosovajob as kosovajob_tasks,
    ofertasuksesi as ofertasuksesi_tasks,
    douglas as douglas_tasks,
    express as express_tasks,
)
from app.utils.tasks import site, scheduler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi_login import LoginManager
from app.models.auth import Register
from datetime import timedelta

app = FastAPI(title="StarLabs API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

site.mount_app(app)

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

templates = Jinja2Templates(directory="app/templates")

class NotAuthenticatedException(Exception):
    pass

def not_authenticated_exception_handler(request, exception):
    response = RedirectResponse(url="/login")
    # response.set_cookie("not_auth", "true")
    response.set_cookie("login_redirect", "true")
    return response

manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)

def check_login_redirect(request):
    if request.cookies.get("login_redirect"):
        return True
    else:
        return False

@app.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    print(request.cookies)
    if check_login_redirect(request):
        params = {"request": request, "login_redirect": True}
        response = templates.TemplateResponse("login.html", params, status_code=status.HTTP_302_FOUND)
        response.delete_cookie("login_redirect")
        return response
    
    elif request.cookies.get("auth") != "None":
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("login.html", {"request": request}, status_code=status.HTTP_200_OK)


@app.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        response = templates.TemplateResponse("login.html", {"request": request, "invalid": True}, status_code=status.HTTP_401_UNAUTHORIZED)
        # response.delete_cookie("not_auth")  # Remove the "not_auth" cookie
        return response
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = manager.create_access_token(data={"sub": user.username}, expires=access_token_expires)
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.get("/register", response_class=HTMLResponse)
def register_html(request: Request):
    if request.cookies.get("auth") != "None":
        print(15)
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
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
    hashed_password = get_hashed_password(password)
    db = SessionLocal()
    existing_username = db.query(Register).filter(Register.username == username).first()
    if existing_username:
        return templates.TemplateResponse("register.html", {"request": request, "username_exists": True})
    
    existing_email = db.query(Register).filter(Register.email == email).first()
    if existing_email:
        return templates.TemplateResponse("register.html", {"request": request, "email_exists": True})
    
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


app.include_router(gjirafa.router)
app.include_router(telegrafi.router)
app.include_router(kosovajob.router)
app.include_router(ofertasuksesi.router)
app.include_router(express.router)
app.include_router(douglas.router)

@app.on_event("startup")
async def startup():
    scheduler.start()

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
