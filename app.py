from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError

from schemas.book_schema import BookSchema, display_book
from schemas.error_schema import ErrorSchema
from models.book import Book
from models import Session

# Definindo infomações básicas.
info = Info(title='Digilibra', version='1.0.0')
app = OpenAPI(__name__, info=info)

# Definindo tags.
book_tag = Tag(name='Book', description='Gerenciamento de livros')


@app.get('/')
def home():
    return redirect('/openapi')

@app.post('/book', tags=[book_tag], responses={'200': BookSchema, '400': ErrorSchema})
def add_book(form: BookSchema):
    '''Adiciona um novo livro e retorna uma apresentação do livro.
    '''
    book = Book(
        name=form.name,
        author=form.author,
        quantity=form.quantity,
        value=form.value,
        release_date=form.release_date
    )

    # TODO: Lógica do BD.
    try:
        session = Session()
        session.add(book)
        session.commit()
        return display_book(book), 200
    except IntegrityError as e:
        return {'message': f'Erro ao adicionar o livro {book.name}: {e}'}, 409
    except Exception as e:
        return {'message': str(e)}, 400

