from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import FileResponse, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from app.models.auth import SignupData
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.utils.database import session

router = APIRouter(tags=["User Data"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "6b305759f35f338a9734cc73a756256b1579fa0248a3f954886dd107e0190ca5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/")
def show_login_form():
    return FileResponse("app/templates/index.html")

@router.get("/register")
def signup_html():
    return FileResponse("app/templates/signup.html")

@router.post("/process-signup")
def process_signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    hashed_password = pwd_context.hash(password)
    new_user = SignupData(username=username, email=email, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"Message": "New account added successfully!"}

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...) ,):
    user = session.query(SignupData).filter(SignupData.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Username not found")
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=404, detail="Invalid password")
    else:
       access_token = generate_token(data={"sub": user.username})
       return {"access_token": access_token, "token_type": "bearer"}
    
def get_current_user(token: Form(...) = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=401, detail="Invalid auth credentials", headers={"WWW-Authenticate": "Bearer"})
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username:str = payload.get("sub")
        if username is None:
            raise credential_exception
        else:
            token_data = TokenData(username=username)
            return token_data
    except JWTError:
        raise credential_exception