from sqlalchemy import Column, Integer, String, Float
from app.utils.database import engine
from app.models import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    price = Column(String(200))