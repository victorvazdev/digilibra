from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from models import Session
from models.author import Author
from schemas.error_schema import ErrorSchema
from schemas.author_schema import *


author_tag = Tag(name='author', description='Gerenciamento de autores.')
author_bp = APIBlueprint('author', __name__, abp_tags=[author_tag])


@author_bp.post('/author', tags=[author_tag], responses={'200': AuthorSchema, '400': ErrorSchema})
def add_author(form: AuthorSchema):
    session = Session()
    author = Author(name=form.name)

    try:
        session.add(author)
        session.commit()

        return {'id': author.id, 'name': author.name}, 200
    except IntegrityError:
        return {'message': 'Autor já existe'}, 409
    except Exception as e:
        return {'message': str(e)}, 400
    
@author_bp.get('/authors', tags=[author_tag], responses={'200': AuthorListSchema, '404': ErrorSchema})
def get_authors():
    session = Session()
    authors = session.query(Author).all()

    if not authors:
        return {'books': []}, 200
    else:
        return display_author_list(authors), 200
    
@author_bp.delete('/author', tags=[author_tag], responses={'200': AuthorDeleteSchema, '404': ErrorSchema})
def delete_author(query: AuthorDeleteSchema):
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
    session = Session()

    db_query = session.query(Author)
    db_query = db_query.filter(Author.id == form.id)
    author = db_query.first()

    if not author:
        return {'message': f'O livro de ID {form.id} não foi encontrado.'}, 404
    
    author.name = form.name

    try:
        session.commit()
        return display_author(author), 200
    except Exception as e:
        return {'message': f'Erro ao atualizar: {str(e)}'}, 400
    
@author_bp.get('/author', tags=[author_tag], responses={'200': AuthorListSchema, '404': ErrorSchema})
def get_author(query: AuthorSearchSchema):
    session = Session()

    db_query = session.query(Author)

    db_query = db_query.filter(Author.id == query.id)

    author = db_query.first()

    if not author:
        return {'message': 'O autor não foi encontrado.'}, 404
    
    return display_author(author), 200
