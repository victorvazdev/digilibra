from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    books = relationship('Book', back_populates='author_rel')

    def __init__(self, name: str):
        self.name = name
