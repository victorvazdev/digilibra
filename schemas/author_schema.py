from pydantic import BaseModel, Field
from typing import List

from models.author import Author


class AuthorSchema(BaseModel):
    '''Define como um novo autor deve ser representado para inserção no banco de dados.
    '''
    name: str = Field('Rafael V. Martins', description='Nome do autor(a).')


class AuthorListSchema(BaseModel):
    '''Define como uma listagem de vários autores será retornada pela API.
    '''
    authors: List[AuthorSchema]


class AuthorDeleteSchema(BaseModel):
    '''Define a estrutura dos dados necessários para realizar a exclusão de um autor.
    '''
    id: int = Field(description='ID do autor(a) a ser deletado.')


class AuthorUpdateSchema(BaseModel):
    '''Define como os dados de um autor devem ser enviados para permitir a sua atualização.
    '''
    id: int = Field(description='ID do autor a ser atualizado.')
    name: str = Field('Madalene J. Oliveira', description='Novo nome do autor.')


class AuthorSearchSchema(BaseModel):
    '''Define a estrutura e os parâmetros necessários para a busca de um autor específico.
    '''
    id: int = Field(1, description='ID do autor(a) a ser buscado.')


def display_author_list(authors: List[Author]):
    '''Retorna uma representação em dicionário de uma lista de objetos Author, 
    formatando cada um para exibição adequada.
    '''
    author_list = []

    for author in authors:
        author_list.append({
            'id': author.id,
            'name': author.name,
        })

    return {'authors': author_list}

def display_author(author: Author):
    '''Retorna uma representação em dicionário do objeto Author.
    '''
    return {
        'id': author.id,
        'name': author.name,
    }
