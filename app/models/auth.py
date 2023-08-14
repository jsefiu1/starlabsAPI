from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.utils.database import engine
from app.models import Base

class Register(Base):
    __tablename__ = "register"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default="user")

class EditLog(Base):
    __tablename__ = 'edit_logs'

    id = Column(Integer, primary_key=True, index=True)
    admin_username = Column(String, index=True)
    edited_user_username = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow) 
    details = Column(String)