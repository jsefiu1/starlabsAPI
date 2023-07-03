from sqlalchemy import Column, Integer, String, DateTime
from app.models import Base


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    details_link = Column(String(500))
    image_link = Column(String(500))
    date_posted = Column(DateTime)
    date_scraped = Column(DateTime)
