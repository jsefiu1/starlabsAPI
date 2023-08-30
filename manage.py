from fastapi import FastAPI, Depends, Form, Request, status, Query, Path, WebSocket, HTTPException
from fastapi.templating import Jinja2Templates
import uvicorn
from app.routers import telegrafi, gjirafa, kosovajob, express, douglas, ofertasuksesi, contact
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
from app.models.auth import Register, EditLog, ChatMessage, APIKey, Contact
from datetime import timedelta
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.routers.api_key import generate_api_key
from app.routers.schemas import ChatMessageSchema, CreateMessageInput
from fastapi.websockets import WebSocketDisconnect 
import jwt
import math
import httpx
import openai
import logging
import time
from httpx import TimeoutException 
import json


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


def get_username_from_token(token: str):
    try:
        secret_key = SECRET_KEY
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        # Kthe emrin e përdoruesit nga të dhënat e tokenit
        username = decoded_token.get("sub")
        return username
    except jwt.ExpiredSignatureError:
        # Tokeni ka skaduar
        # return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        # return templates.TemplateResponse("home.html", {"request": request})
        return None
    except jwt.InvalidTokenError:
        # Tokeni është i pavlefshëm ose i korruptuar
        # return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        # return templates.TemplateResponse("home.html", {"request": request})
        return None

def get_username_from_request(request: Request):
    access_token = request.cookies.get("auth")
    if access_token:
        username = get_username_from_token(access_token)
        return username

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

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

def get_current_user_role(request: Request):
    access_token = request.cookies.get("auth")
    if access_token:
        username = get_username_from_token(access_token)
        if username:
            db = SessionLocal()
            user = db.query(Register).filter(Register.username == username).first()
            if user:
                return {
                    "role": user.role
                }
    return None
    

def has_admin_role(request: Request):
    user_role = get_current_user_role(request)
    if user_role and user_role.get("role") == "admin":
        return True
    return False


@app.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    print(request.cookies)
    if check_login_redirect(request):
        params = {"request": request, "login_redirect": True}
        response = templates.TemplateResponse("login.html", params, status_code=status.HTTP_302_FOUND)
        response.delete_cookie("login_redirect")
        return response
    
    elif request.cookies.get("auth") != "None" and request.cookies.get("auth"):
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
    print(request.cookies)
    if request.cookies.get("auth") != "None" and request.cookies.get("auth"):
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
def data(request: Request, db: Session = Depends(get_db), user: Register = Depends(manager)):
    username = get_username_from_request(request)
    api_key_entry = db.query(APIKey).filter(APIKey.username == username).first()

    if api_key_entry:
        api_key = api_key_entry.key
        navigation_items = [
            {"name": "Dashboard", "url": "/data"},
            {"name": "Telegrafi", "url": "/telegrafi/view"},
            {"name": "Gjirafa", "url": "/gjirafa/view"},
            {"name": "ofertasuksesi", "url": "/ofertasuksesi/html"},
            {"name": "Douglas", "url": "/douglas/view"},
            {"name": "Kosovajobs", "url": "/kosovajobs/view"},
            {"name": "Express", "url": "/gazetaexpress/view"}
        ]
        return templates.TemplateResponse(
            "data.html", {"request": request, "navigation_items": navigation_items, "user": user, "api_key": api_key}
        )
    else:
        raise HTTPException(status_code=401, detail="Invalid API key or user not found")

        
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    return templates.TemplateResponse("home.html", {"request": request, "username": username, 
                                "user_role": user_role})

#########################USERS#####################################################
@app.get("/users", response_class=HTMLResponse)
def read_users(request: Request, user: Register =  Depends(manager)):
    username = get_username_from_request(request)
    db = SessionLocal()
    users = db.query(Register).all()
    user_role = get_current_user_role(request)
    if has_admin_role(request):
        return templates.TemplateResponse("users.html", {"request": request, "users": users, 
                                    "username": username, "user": user, "user_role": user_role})
    else:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.post("/search", response_class=RedirectResponse)
def search_user(search_username: str = Form(...), user: Register = Depends(manager)):
    return RedirectResponse("/users/" + search_username, status_code=status.HTTP_302_FOUND)

@app.get("/users/{search_username}", response_class=HTMLResponse)
def search_user_by_username(request: Request, search_username: str = Path(...), user: Register = Depends(manager)):
    db = SessionLocal()
    username = get_username_from_request(request)
    user_name = db.query(Register).filter(Register.username == search_username).all()
    user_role = get_current_user_role(request)
    if has_admin_role(request):
        if not user_name:
            return templates.TemplateResponse("search.html", {"request": request, "user_name": user_name, "username": username, "user": user,
                                            "invalid_username": True, "user_role": user_role},
                                            status_code=status.HTTP_404_NOT_FOUND)
        return templates.TemplateResponse("search.html", {"request": request, "user_name": 
                                        user_name, "username": username, "user": user, "user_role": user_role})
    else:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
#################################################################################################################
@app.get("/profile", response_class=HTMLResponse)
def user_profile(request: Request, user: Register = Depends(manager), user_data: dict = Depends(get_current_user_data)):
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    return templates.TemplateResponse("profile.html", {"request": request, "username": username, 
                                    "user": user, "user_data": user_data, "user_role": user_role})

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
    user_role = get_current_user_role(request)
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        db.commit()
        db.refresh(user)
        return templates.TemplateResponse("profile.html", {"request": request, "username": username, 
                    "user": user, "user_data": form_data, "success_message": True, "user_role": user_role})
    else:
        return templates.TemplateResponse("profile.html", {"request": request, "username": username, 
                        "user": user, "user_data": form_data, "error_message": True, "user_role": user_role})

@app.get("/profile/change-password", response_class=HTMLResponse)
def change_password_view(request: Request, user: Register = Depends(manager)):
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    return templates.TemplateResponse("password.html", {"request": request, 
                                    "username": username, "user_role": user_role})

@app.post("/profile/change-password", response_class=HTMLResponse)
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
        user_role = get_current_user_role(request)
        db.commit()
        db.refresh(user)
        return templates.TemplateResponse("password.html", {"request": request, "username": username, 
                                        "success_message": True, "user_role": user_role})
    else:
        return templates.TemplateResponse("password.html", {"request": request, "username": username, 
                                        "error_message": True, "user_role": user_role})

###############################USERS###################################################
@app.get("/users/edit-user/{user_id}")
def edit_user(request: Request, user_id: int, user: Register = Depends(manager)):
    db = SessionLocal()
    db_user = db.query(Register).filter(Register.id == user_id).first()
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    if has_admin_role(request):
        return templates.TemplateResponse("edit_user.html", {"request": request, "username": username, 
                                "db_user": db_user, "user": user, "user_role": user_role})
    else:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.post("/users/edit-user/{user_id}")
def save_edit(user_id: int, request: Request, user: Register = Depends(manager),
              first_name: str = Form(...),
              last_name: str = Form(...),
              edit_username: str = Form(...),
              email: str = Form(...)):
    db = SessionLocal()
    db_user = db.query(Register).filter(Register.id == user_id).first()
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    if has_admin_role(request):
        if db_user:
            db_user.first_name = first_name
            db_user.last_name = last_name
            db_user.username = edit_username
            db_user.email = email
            db.commit()
            admin_username = get_username_from_request(request) 
            edit_log = EditLog(
                admin_username=admin_username,
                edited_user_username=db_user.username,
                details=f"Updated user info: first_name={first_name}, last_name={last_name}, username={edit_username}, email={email}"
            )

            db.add(edit_log)
            db.commit()
            return templates.TemplateResponse("edit_user.html", {"request": request, "username": username, 
                            "db_user": db_user,"user": user, "success_message": True, "user_role": user_role})
    else:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("edit_user.html", {"request": request, "username": username, 
                                    "user": user,"success_message": False, "user_role": user_role})
    

@app.get("/delete/{user_id}")
def delete_user(request: Request, user_id: int):
    db = SessionLocal()
    user = db.query(Register).filter(Register.id == user_id).first()
    admin_username = get_username_from_request(request)  # Get the admin's username
    if has_admin_role(request):
        if user:
            log_details = f"Deleted user account: username={user.username}"
            edit_log = EditLog(
                admin_username=admin_username,
                edited_user_username=user.username, 
                details=log_details
            )
            db.add(edit_log)
            
            db.delete(user)
            db.commit()

        return RedirectResponse("/users")
    else:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

#######################LOGS##########################################################
@app.get("/logs", response_class=HTMLResponse)
def display_logs_or_search(
    request: Request, 
    user: Register = Depends(manager),
    user_affected: str = Query(None),
    page: int = Query(default=1, title="Page number"),
):
    user_role = get_current_user_role(request)
    username = get_username_from_request(request)

    if not has_admin_role(request):
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    db = SessionLocal()
    items_per_page = 5 
    
    query = db.query(EditLog)

    if user_affected:  # If user_affected is provided, perform a search
        logs = query.filter(EditLog.edited_user_username == user_affected).all()
    else: 
        logs = query.all()

    total_items = len(logs)
    total_pages = (total_items + items_per_page - 1)

    offset = (page - 1) * items_per_page
    logs_to_display = logs[offset:offset + items_per_page]
    
    template_vars = {
        "logs": logs_to_display,
        "user_affected": user_affected,
        "username": username,
        "user_role": user_role,
        "current_page": page,
        "total_pages": total_pages,
    }

    return templates.TemplateResponse("logs.html", {"request": request, **template_vars})



####################### OPEN AI ###############################################################

openai_api_key = "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"
messages = [{"role": "system", "content": "You are a programmer or Developer"}]

@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request, user: Register = Depends(manager)):
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    return templates.TemplateResponse("chat.html", {"request": request, "username": username, "user_role": user_role})

@app.post("/chat")
async def custom_chat(user_input: str = Form(...)):
    messages.append({"role": "user", "content": user_input})

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                },
                auth=("", openai_api_key),
                timeout=httpx.Timeout(30),
            )
            response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            chatgpt_reply = response_data["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": chatgpt_reply})
            return {"response": chatgpt_reply}
        else:
            return {"response": "No valid response from the model"}

    except (httpx.RequestError, TimeoutException, json.JSONDecodeError) as e:
        error_message = "An error occurred while processing the request: " + str(e)
        return {"error": error_message}

    
    
    
########################################WEB SOCKET#############################################

clients = []

@app.websocket("/messages")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket.accept()

    query_params = websocket.query_params
    username = query_params.get("username")

    print(f"WebSocket connection opened for user: {username}")

    clients.append((username, websocket))

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from user {username}: {data}")

            db = SessionLocal()
            try:
                new_message = create_message(db, username, data)
                print(f"Created new message in database: {new_message.message}")
            finally:
                db.close()

            message = {
                "username": username,
                "message": new_message.message,
                "timestamp": new_message.timestamp
            }

            message_json = json.dumps(message)

            for client_username, client_websocket in clients:
                await client_websocket.send_text(message_json)
                print(f"Sent message to client {client_username}")
    except WebSocketDisconnect:
        for client_tuple in clients:
            if client_tuple[0] == username:
                clients.remove(client_tuple)
                print(f"WebSocket connection closed for user: {username}")
                break



@app.get("/messages", response_class=HTMLResponse)
async def message(request: Request,  user: Register = Depends(manager)):
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)    
    if not has_admin_role(request):
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("messages.html", {"request": request, "username": username, "user_role": user_role})


def create_message(db: Session, username: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = db.query(Register).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with username '{username}' not found.")
    new_message = ChatMessage(message=message, timestamp=timestamp, user=user)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

            
@app.get("/api/messages", response_model=List[ChatMessageSchema])
async def get_messages(username: str = Depends(get_username_from_request), db: Session = Depends(get_db)):
    try:
        messages = db.query(ChatMessage).order_by(ChatMessage.timestamp).all()
        return messages
    except Exception as e:
        print(f"Error retrieving messages: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving messages")

#################################################################################################################
########## GENERATE API KEY #############

@app.get("/generate-api-key", response_class=HTMLResponse)
async def generate_api_key_html(request: Request, user: Register = Depends(manager)):
    db = SessionLocal()
    username = get_username_from_request(request)

    api_key_entry = db.query(APIKey).filter(APIKey.username == username).first()

    if api_key_entry:
        api_key = api_key_entry.key
    else:
        api_key = "API key not found"
    
    user_role = get_current_user_role(request)       
    
    template_params = {"request": request, "username": username, "user_role": user_role, "api_key": api_key}
    
    return templates.TemplateResponse("generate_api_key.html", template_params)


@app.post('/generate-api-key')
async def generate_api_key_router(request: Request):
    username = get_username_from_request(request)
    new_api_key = generate_api_key(request)

    db = SessionLocal()

    existing_api_key = db.query(APIKey).filter_by(username=username).first()

    if existing_api_key:
        existing_api_key.key = new_api_key
    else:
        api_key = APIKey(username=username, key=new_api_key)
        db.add(api_key)

    db.commit()

    return {"key": new_api_key}


@app.exception_handler(HTTPException)
async def redirect_invalid_api_key(request, exc):
    if exc.status_code == 401:
        return RedirectResponse("/generate-api-key", status_code=302)
    return exc


############################################# CONTACT FORM ################################################
####


app.include_router(contact.router)

@app.get("/contact-messages", response_class=HTMLResponse)
async def list_contact_messages(
    request: Request,
    db: Session = Depends(get_db),
    search_query: str = Query(default="", title="Search Query"),
):
    username = get_username_from_request(request)
    user_role = get_current_user_role(request)
    
    items_per_page = 5 

    query = db.query(Contact)

    if search_query:
        query = query.filter(Contact.name.ilike(f"%{search_query}%") | Contact.email.ilike(f"%{search_query}%"))

    contact_messages = query.all()

    template_vars = {"contact_messages": contact_messages, "search_query": search_query, "username": username,
                     "user_role": user_role}
    return templates.TemplateResponse("contactmessages.html", {"request": request, **template_vars})
####
###########################################################################################################

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
