from sqlalchemy import Column, Integer,Text
from app.models import Base

class Job(Base):
    __tablename__='jobs'
    id = Column(Integer, primary_key=True)
    image_url = Column(Text)
    title = Column(Text)
    city = Column(Text)
    expires_date = Column(Text)
    date_of_scrape=Column(Text)
