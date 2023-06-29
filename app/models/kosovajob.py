from sqlalchemy import Column, Integer,Text
from app.models import Base

class Job(Base):
    __tablename__='jobs'
    id=Column(Integer,primary_key=True)
    title=Column(Text)
    city=Column(Text)
    expire_date = Column(Text)
