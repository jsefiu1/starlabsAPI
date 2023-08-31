from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.auth import Register
from app.models import Base  

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    
    user_id = Column(Integer, ForeignKey("register.id"))
    user = relationship("Register", back_populates="review")
