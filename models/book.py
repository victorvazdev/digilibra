from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models.base import Base


class Book(Base):
    __tablename__ = 'book'

    id = Column('pk_book', Integer, primary_key=True)
    name = Column(String(100))
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    quantity = Column(Integer)
    value = Column(Float)
    release_date = Column(Date)
    insertion_date = Column(DateTime, default=datetime.now())
    author_rel = relationship('Author', back_populates='books')

    def __init__(self, name:str, author_id:int, quantity:int, value:float, release_date:Date, insertion_date:Union[DateTime, None] = None):
        '''Cria um livro

        Argumentos:
            name: Nome do livro.
            author: Autor do livro.
            quantity: Quantidade disponível de livros.
            value: Preço do livro
            release_date: Data de lançamento do livro.
            insertion_date: Data de adição do livro na biblioteca.
        '''
        self.name = name
        self.author_id = author_id
        self.quantity = quantity
        self.value = value
        self.release_date = release_date

        # Caso a data de adição for informada, ela será configurada ao invés da data atual.
        if insertion_date:
            self.insertion_date = insertion_date            
