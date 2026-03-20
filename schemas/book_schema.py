from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from models.book import Book

class BookSchema(BaseModel):
    '''Define como um novo livro a ser inserido deve ser representado.
    '''
    name: str = Field("Clean Code")
    author: str = Field("Robert C. Martin")
    quantity: Optional[int] = Field(10)
    value: float = Field(289.6)
    release_date: Optional[date] = Field(default=date(2025, 10, 12))

def display_book(book: Book):
    '''Retorna uma representação do livro seguindo o schema definido
    '''
    return {
        'id': book.id,
        'name': book.name,
        'quantity': book.quantity,
        'value': book.value,
        'release_date': book.release_date
    }
