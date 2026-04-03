from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from models import Session
from models.author import Author
from schemas.error_schema import ErrorSchema
from schemas.author_schema import *

author_tag = Tag(name='author', description='Gerenciamento de autores.')
author_bp = APIBlueprint('author', __name__, abp_tags=[author_tag])


@author_bp.post('/author', tags=[author_tag], responses={'201': AuthorSchema, '400': ErrorSchema})
def add_author(form: AuthorSchema):
    '''Cadastra um novo autor no sistema.
    
    Recebe os dados do autor e tenta salvá-lo no banco de dados. 
    Retorna erro 409 caso já exista um autor com o mesmo nome exato cadastrado.
    '''
    session = Session()
    author = Author(name=form.name)

    try:
        session.add(author)
        session.commit()

        return {'id': author.id, 'name': author.name}, 201
    except IntegrityError:
        return {'message': 'Autor já existe'}, 409
    except Exception as e:
        return {'message': str(e)}, 400


@author_bp.get('/authors', tags=[author_tag], responses={'200': AuthorListSchema, '404': ErrorSchema})
def get_authors():
    '''Lista todos os autores cadastrados.
    
    Retorna uma lista contendo os detalhes de todos os autores no banco de dados. 
    Se não houver nenhum autor, retorna uma lista vazia.
    '''
    session = Session()
    authors = session.query(Author).all()

    if not authors:
        return {'authors': []}, 200
    else:
        return display_author_list(authors), 200


@author_bp.delete('/author', tags=[author_tag], responses={'200': AuthorDeleteSchema, '404': ErrorSchema})
def delete_author(query: AuthorDeleteSchema):
    '''Remove um autor do sistema.
    
    Busca um autor pelo seu ID e realiza a exclusão. 
    Retorna erro 404 caso o ID fornecido não seja encontrado.
    '''
    session = Session()

    db_query = session.query(Author)
    db_query = db_query.filter(Author.id == query.id)
    author = db_query.first()
    author_deleted = db_query.delete()
    session.commit()

    if author_deleted:
        return {'message': f'O autor {author.name} de ID {author.id} foi removido com sucesso'}, 200
    else:
        return {'message': f'O autor de ID {query.id} não foi encontrado.'}, 404


@author_bp.put('/update_author', tags=[author_tag], responses={'200': AuthorListSchema, '404': ErrorSchema})
def update_author(form: AuthorUpdateSchema):
    '''Atualiza os dados de um autor existente.
    
    Busca o autor pelo ID informado e atualiza o seu nome. 
    Retorna erro 404 caso o autor não exista no banco de dados.
    '''
    session = Session()

    db_query = session.query(Author)
    db_query = db_query.filter(Author.id == form.id)
    author = db_query.first()

    if not author:
        return {'message': f'O autor de ID {form.id} não foi encontrado.'}, 404
    
    author.name = form.name

    try:
        session.commit()
        return display_author(author), 200
    except Exception as e:
        return {'message': f'Erro ao atualizar: {str(e)}'}, 400


@author_bp.get('/author', tags=[author_tag], responses={'200': AuthorListSchema, '404': ErrorSchema})
def get_author(query: AuthorSearchSchema):
    '''Busca os detalhes de um autor específico.
    
    Pesquisa no banco de dados pelo ID fornecido e retorna os dados do autor. 
    Retorna erro 404 se nenhum autor for encontrado com o ID especificado.
    '''
    session = Session()

    db_query = session.query(Author)
    db_query = db_query.filter(Author.id == query.id)
    author = db_query.first()

    if not author:
        return {'message': 'O autor não foi encontrado.'}, 404
    
    return display_author(author), 200
