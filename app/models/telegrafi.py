from sqlalchemy import Column, Integer, String
from app.utils.database import engine
from app.models import Base


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    details_link = Column(String(500))
    image_link = Column(String(500))
