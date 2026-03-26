from pydantic import BaseModel, Field
from typing import Optional, List

from models.author import Author


class AuthorSchema(BaseModel):
    name: str = Field('Rafael V. Martins', description='Nome do autor(a).')

class AuthorListSchema(BaseModel):
    books: List[AuthorSchema]

class AuthorDeleteSchema(BaseModel):
    id: int = Field(description='ID do autor(a) a ser deletado.')

class AuthorUpdateSchema(BaseModel):
    id: int = Field(description='ID do livro a ser atualizado.')
    name: str = Field('Madalene J. Oliveira', description='Novo nome do autor.')

class AuthorSearchSchema(BaseModel):
    id: int = Field(1, description='ID do autor(a) a ser buscado.')


def display_author_list(authors: List[Author]):
    author_list = []

    for author in authors:
        author_list.append({
            'id': author.id,
            'name': author.name,
        })

    return {'authors': author_list}

def display_author(author: Author):
    return {
        'id': author.id,
        'name': author.name,
    }
