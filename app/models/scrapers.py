from sqlalchemy import Column, Integer, String, Float, Boolean
from app.utils.database import engine
from app.models import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float)
    details_link = Column(String(500))
    discount_price = Column(Float, nullable=True)
    image_link = Column(String(500))
    is_risi = Column(Boolean)
    is_24h = Column(Boolean)


Base.metadata.create_all(engine)
