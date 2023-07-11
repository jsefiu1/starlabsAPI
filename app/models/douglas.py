from sqlalchemy import Column, Integer, String, DateTime, Float
from app.utils.database import engine
from app.models import Base

class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    category = Column(String(200))
    price = Column(String(200))
    details_link = Column(String(500))
    date_scraped = Column(DateTime)