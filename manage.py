from fastapi import FastAPI, Depends, Form, Request, status, Query, Path
from fastapi.templating import Jinja2Templates
import uvicorn
from app.routers import telegrafi, gjirafa, kosovajob, express, douglas, ofertasuksesi, users
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
import jwt

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


# Funksioni për të kthyer emrin e përdoruesit nga tokeni
def get_username_from_token(token: str):
    try:
        # Vendosni çelësin sekret të tokenit që keni përdorur për të nënshkruar tokenin në kodin tuaj
        secret_key = SECRET_KEY
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        # Kthe emrin e përdoruesit nga të dhënat e tokenit
        username = decoded_token.get("sub")
        return username
    except jwt.ExpiredSignatureError:
        # Tokeni ka skaduar
        return None
        # return templates.TemplateResponse("home.html", {"request": request})
    except jwt.InvalidTokenError:
        # Tokeni është i pavlefshëm ose i korruptuar
        return None
        # return templates.TemplateResponse("home.html", {"request": request})

def get_username_from_request(request: Request):
    access_token = request.cookies.get("auth")
    if access_token:
        # Kërko emrin e përdoruesit duke përdorur token-in
        username = get_username_from_token(access_token)
        return username

    return None

def get_user_id_from_username(username: str):
    db = SessionLocal()
    user = db.query(Register.id).filter(Register.username == username).first()
    if user:
        return user.id
    return None

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

def get_plain_password(hashed_password):
    return pwd_context.hash(hashed_password)

def get_current_user_data(request: Request):
    access_token = request.cookies.get("auth")
    if access_token:
        username = get_username_from_token(access_token)
        if username:
            db = SessionLocal()
            user = db.query(Register).filter(Register.username == username).first()
            if user:
                return {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "password": get_plain_password(user.password)
                }
    return None

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


@app.get("/data", response_class=HTMLResponse)
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
        
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = get_username_from_request(request)
    return templates.TemplateResponse("home.html", {"request": request, "username": username})

@app.get("/users", response_class=HTMLResponse)
def read_users(request: Request, user: Register =  Depends(manager)):
    username = get_username_from_request(request)
    db = SessionLocal()
    users = db.query(Register).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "username": username, "user": user})

@app.post("/search", response_class=RedirectResponse)
def search_user(search_username: str = Form(...), user: Register = Depends(manager)):
    return RedirectResponse("/users/" + search_username, status_code=status.HTTP_302_FOUND)

@app.get("/users/{search_username}", response_class=HTMLResponse)
def search_user_by_username(request: Request, search_username: str = Path(...), user: Register = Depends(manager)):
    db = SessionLocal()
    username = get_username_from_request(request)
    user_name = db.query(Register).filter(Register.username == search_username).all()
    if not user_name:
        return templates.TemplateResponse("search.html", {"request": request, "user_name": user_name, "username": username, "user": user}, 
                                          status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("search.html", {"request": request, "user_name": user_name, "username": username, "user": user})

@app.get("/profile", response_class=HTMLResponse)
def user_profile(request: Request, user: Register = Depends(manager), user_data: dict = Depends(get_current_user_data)):
    username = get_username_from_request(request)
    return templates.TemplateResponse("profile.html", {"request": request, "username": username, "user": user, "user_data": user_data})

@app.post("/profile", response_class=HTMLResponse)
async def update_user_profile(request: Request, user: Register = Depends(manager)):
    username = get_username_from_request(request)
    id = get_user_id_from_username(username)
    form_data = await request.form()
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")
    username = form_data.get("username")
    email = form_data.get("email")

    # Bejme update te dhenat ne databaze
    db = SessionLocal()
    user = db.query(Register).filter(Register.id == id).first()
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        db.commit()
        db.refresh(user)
        return templates.TemplateResponse("profile.html", {"request": request, "username": username, "user": user, "user_data": form_data, "success_message": True})
    else:
        return templates.TemplateResponse("profile.html", {"request": request, "username": username, "user": user, "user_data": form_data, "error_message": True})

@app.get("/change-password", response_class=HTMLResponse)
def change_password_view(request: Request, user: Register = Depends(manager)):
    username = get_username_from_request(request)
    return templates.TemplateResponse("password.html", {"request": request, "username": username})

@app.post("/change-password", response_class=HTMLResponse)
def change_user_password(request: Request, user: Register = Depends(manager),
                         new_password: str = Form(...),
                         confirm_password: str = Form(...),):
    
    username = get_username_from_request(request)
    user_id = get_user_id_from_username(username)
    
    if new_password == confirm_password:
        db = SessionLocal()
        user = db.query(Register).filter(Register.id == user_id).first()
        new_hashed_Password = get_hashed_password(new_password)
        user.password = new_hashed_Password
        db.commit()
        db.refresh(user)
        return templates.TemplateResponse("password.html", {"request": request, "username": username, "success_message": True})
    else:
        return templates.TemplateResponse("password.html", {"request": request, "username": username, "error_message": True})

@app.get("/edit-user/{user_id}")
def edit_user(request: Request, user_id: int):
    db = SessionLocal()
    user = db.query(Register).filter(Register.id == user_id).first()
    username = get_username_from_request(request)
    return templates.TemplateResponse("edit_user.html", {"request": request, "username": username, "user": user})

@app.post("/edit-user/{user_id}")
def save_edit(user_id: int, request: Request,
              first_name: str = Form(...),
              last_name: str = Form(...),
              edit_username: str = Form(...),
              email: str = Form(...)):
    db = SessionLocal()
    user = db.query(Register).filter(Register.id == user_id).first()
    username = get_username_from_request(request)
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.username = edit_username
        user.email = email
        db.commit()
        return templates.TemplateResponse("edit_user.html", {"request": request, "username": username, "user": user, "success_message": True})
    
    return templates.TemplateResponse("edit_user.html", {"request": request, "username": username, "user": user,"success_message": False})
    

@app.get("/delete/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(Register).filter(Register.id == user_id).first()

    if user:
        db.delete(user)
        db.commit()

    return RedirectResponse("/users")


@app.get("/logout", response_class=RedirectResponse)
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
