from sqlalchemy import Column, Integer, String, Date

from database import Base


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    headline = Column(String)
    text = Column(String)
    created = Column(Date)
