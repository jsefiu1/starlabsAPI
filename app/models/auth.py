from sqlalchemy import Column, Integer, String, DateTime, Float
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