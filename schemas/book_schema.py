from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date

from models.book import Book

class BookSchema(BaseModel):
    name: str = Field('Como Treinar Bíceps', description='Nome do livro.')
    author_id: int = Field(1, description='ID do autor(a) do livro no sistema.')
    quantity: Optional[int] = Field(10, description='Quantidade disponível para o livro.')
    value: float = Field(289.6, description='Preço do livro.')
    release_date: Optional[date] = Field(default=date(2025, 10, 12), description='Data de publicação do livro.')

class BookListSchema(BaseModel):
    books: List[BookSchema]

class BookSearchSchema(BaseModel):
    name: str = Field('Como Treinar Bíceps', description='Nome do livro a ser buscado.')
    author_id: int = Field(1, description='ID do autor do livro a ser buscado.')

class BookDeleteSchema(BaseModel):
    id: int = Field(description='ID do livro a ser deletado.')

class BookUpdateSchema(BaseModel):
    id: int = Field(description='ID do livro a ser atualizado.')
    name: Optional[str] = Field(None, description='Novo nome do livro.')
    author_id: Optional[int] = Field(None, description='ID do novo autor(a) do livro.')
    quantity: Optional[int] = Field(None, description='Nova quantidade disponível para o livro.')
    value: Optional[float] = Field(None, description='Novo preço do livro.')
    release_date: Optional[date] = Field(None, description='Nova data de publicação do livro.')

    # Validador para converter strings "null" ou vazias em None
    @field_validator('name', 'author_id', 'quantity', 'value', 'release_date', mode='before')
    @classmethod
    def empty_to_none(cls, v):
        if v == "null" or v == "":
            return None
        return v

def display_book(book: Book):
    return {
        'id': book.id,
        'name': book.name,
        'author': book.author_rel.name if book.author_rel else 'Desconhecido',
        'quantity': book.quantity,
        'value': book.value,
        'release_date': book.release_date
    }

def display_book_list(books: List[Book]):
    book_list = []

    for book in books:
        book_list.append({
            'id': book.id,
            'name': book.name,
            'author': book.author_rel.name if book.author_rel else 'Desconhecido',
            'quantity': book.quantity,
            'value': book.value,
            'release_date': book.release_date
        })

    return {'books': book_list}
