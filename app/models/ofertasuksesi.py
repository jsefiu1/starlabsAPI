from sqlalchemy import Column, Integer, String, Text
from app.models import Base

class Data(Base):
    __tablename__ = "oferta"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    info = Column(String)
    location = Column(String)
    image = Column(Text)