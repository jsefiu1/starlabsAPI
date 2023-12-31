from sqlalchemy import Column, Integer, String, Float, DateTime
from app.models import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    price = Column(Float)
    details_link = Column(String(500))
    date_scraped = Column(DateTime)
