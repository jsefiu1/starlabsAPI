from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.utils.database import engine
from app.models import Base

class Register(Base):
    __tablename__ = "register"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True) 
    email = Column(String)
    password = Column(String)
    role = Column(String, default="user")
    messages = relationship("ChatMessage", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")  

class EditLog(Base):
    __tablename__ = 'edit_logs'

    id = Column(Integer, primary_key=True, index=True)
    admin_username = Column(String, index=True)
    edited_user_username = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow) 
    details = Column(String)
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True)
    message = Column(String)
    timestamp = Column(String)
    username = Column(String, ForeignKey("register.username")) 
    user = relationship("Register", back_populates="messages")
    
class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey('register.username'))
    key = Column(String, unique=True, index=True)
    user = relationship("Register", back_populates="api_keys")

class Contact(Base):
    __tablename__ = "text"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)
    role = Column(String, default="user")
