from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, default='Generic')
    published = Column(Boolean, default=True)
    # created_at = Column(DateTime, nullable=False)