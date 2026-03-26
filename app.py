from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError

from schemas.book_schema import *
from schemas.error_schema import ErrorSchema
from schemas.author_schema import *
from models.book import Book
from models.author import Author
from models import Session

info = Info(title='Digilibra', version='1.0.0')
app = OpenAPI(__name__, info=info)

book_tag = Tag(name='Book', description='Gerenciamento de livros.')
author_tag = Tag(name='Author', description='Gerenciamento de autores.')


@app.get('/')
def home():
    return redirect('/openapi/swagger')


@app.post('/book', tags=[book_tag], responses={'200': BookSchema, '400': ErrorSchema})
def add_book(form: BookSchema):
    session = Session()
    book = Book(
        name=form.name,
        author_id=form.author_id,
        quantity=form.quantity,
        value=form.value,
        release_date=form.release_date
    )

    author = session.query(Author).filter(Author.id == form.author_id).first()
    if not author:
        return {'message': 'Autor não encontrado. Crie o autor primeiro.'}, 404

    try:
        session.add(book)
        session.commit()
        return display_book(book), 200
    except IntegrityError as e:
        return {'message': f'Erro ao adicionar o livro {book.name}: {e}'}, 409
    except Exception as e:
        return {'message': str(e)}, 400


@app.get('/books', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def get_books():
    session = Session()
    books = session.query(Book).all()

    if not books:
        return {'books': []}, 200
    else:
        return display_book_list(books), 200


@app.get('/book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def get_book(query: BookSearchSchema):
    session = Session()

    db_query = session.query(Book)

    db_query = db_query.filter(Book.name == query.name)
    db_query = db_query.filter(Book.author_id == query.author_id)

    book = db_query.first()

    if not book:
        return {'message': 'O livro não foi encontrado.'}, 404
    
    return display_book(book), 200

  
@app.delete('/book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def delete_book(query: BookDeleteSchema):
    session = Session()

    db_query = session.query(Book)
    db_query = db_query.filter(Book.id == query.id)
    book = db_query.first()
    book_deleted = db_query.delete()
    session.commit()

    if book_deleted:
        return {'message': f'Livro {book.name} de {book.author} foi removido com sucesso'}, 200
    else:
        return {'message': f'O livro de ID {query.id} não foi encontrado.'}, 404
    

@app.put('/update_book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def update_book(form: BookUpdateSchema):
    session = Session()

    db_query = session.query(Book)
    db_query = db_query.filter(Book.id == form.id)
    book = db_query.first()

    if not book:
        return {'message': f'O livro de ID {form.id} não foi encontrado.'}, 404

    if form.author_id is not None:
        author = session.query(Author).filter(Author.id == form.author_id).first()
        
        if not author:
            return {'message': 'Autor não encontrado. Crie o autor primeiro.'}, 404
    
    book.name = form.name if form.name is not None else book.name
    book.author_id = form.author_id if form.author_id is not None else book.author_id
    book.quantity = form.quantity if form.quantity is not None else book.quantity
    book.value = form.value if form.value is not None else book.value
    book.release_date = form.release_date if form.release_date is not None else book.release_date

    try:
        session.commit()
        return display_book(book), 200
    except Exception as e:
        return {'message': f'Erro ao atualizar: {str(e)}'}, 400
    
@app.post('/author', tags=[author_tag], responses={'200': AuthorSchema, '400': ErrorSchema})
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
    
@app.get('/authors', tags=[author_tag], responses={'200': AuthorListSchema, '404': ErrorSchema})
def get_authors():
    session = Session()
    authors = session.query(Author).all()

    if not authors:
        return {'books': []}, 200
    else:
        return display_author_list(authors), 200
    
@app.delete('/author', tags=[author_tag], responses={'200': AuthorDeleteSchema, '404': ErrorSchema})
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
    
@app.put('/update_author', tags=[author_tag], responses={'200': BookListSchema, '404': ErrorSchema})
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
    
@app.get('/author', tags=[author_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def get_author(query: AuthorSearchSchema):
    session = Session()

    db_query = session.query(Author)

    db_query = db_query.filter(Author.id == query.id)

    author = db_query.first()

    if not author:
        return {'message': 'O autor não foi encontrado.'}, 404
    
    return display_author(author), 200