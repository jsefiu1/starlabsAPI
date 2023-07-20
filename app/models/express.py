from sqlalchemy import Column, Integer, String, DateTime
from app.models import Base

class Lajme(Base):
    __tablename__ = "lajme"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    name2 = Column(String(200))
    details = Column(String(500))
    image = Column(String(500))
    date_scraped = Column(DateTime)