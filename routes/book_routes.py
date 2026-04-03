from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from models import Session
from models.book import Book
from models.author import Author
from schemas.book_schema import *
from schemas.error_schema import ErrorSchema

book_tag = Tag(name='book', description='Gerenciamento de livros.')
book_bp = APIBlueprint('book', __name__, abp_tags=[book_tag])


@book_bp.post('/book', tags=[book_tag], responses={'201': BookSchema, '400': ErrorSchema})
def add_book(form: BookSchema):
    '''Cadastra um novo livro no acervo.
    
    Verifica primeiro se o ID do autor (author_id) fornecido existe no sistema. 
    Se não existir, retorna erro 404. Caso exista, prossegue com a criação do livro.
    '''
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
        return display_book(book), 201
    except IntegrityError as e:
        return {'message': f'Erro ao adicionar o livro {book.name}: {e}'}, 409
    except Exception as e:
        return {'message': str(e)}, 400


@book_bp.get('/books', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def get_books():
    '''Lista todos os livros cadastrados no acervo.
    
    Retorna os detalhes de todos os livros, incluindo o nome do autor mapeado 
    através do relacionamento. Retorna uma lista vazia caso o acervo não tenha livros.
    '''
    session = Session()
    books = session.query(Book).all()

    if not books:
        return {'books': []}, 200
    else:
        return display_book_list(books), 200


@book_bp.get('/book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def get_book(query: BookSearchSchema):
    '''Busca os detalhes de um livro específico.
    
    Pesquisa no banco de dados filtrando pelo nome do livro E pelo ID do autor. 
    Retorna erro 404 se a combinação informada não for encontrada.
    '''
    session = Session()

    db_query = session.query(Book)
    db_query = db_query.filter(Book.name == query.name)
    db_query = db_query.filter(Book.author_id == query.author_id)

    book = db_query.first()

    if not book:
        return {'message': 'O livro não foi encontrado.'}, 404
    
    return display_book(book), 200

  
@book_bp.delete('/book', tags=[book_tag], responses={'200': BookDeleteSchema, '404': ErrorSchema})
def delete_book(query: BookDeleteSchema):
    '''Remove um livro do acervo.
    
    Busca o livro pelo seu ID e realiza a exclusão no banco de dados. 
    Retorna erro 404 caso o ID fornecido não seja encontrado.
    '''
    session = Session()

    db_query = session.query(Book)
    db_query = db_query.filter(Book.id == query.id)
    book = db_query.first()
    author_name = book.author_rel.name if book.author_rel else 'Desconhecido'
    book_deleted = db_query.delete()
    session.commit()

    if book_deleted:
        return {'message': f'Livro {book.name} de {author_name} (ID: {book.author_id}) foi removido com sucesso'}, 200
    else:
        return {'message': f'O livro de ID {query.id} não foi encontrado.'}, 404
    

@book_bp.put('/update_book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def update_book(form: BookUpdateSchema):
    '''Atualiza os dados de um livro existente.
    
    Busca o livro pelo ID e atualiza os campos fornecidos. Se um novo author_id for 
    enviado, verifica se o autor correspondente existe antes de efetuar a atualização.
    Retorna erro 404 caso o livro ou o novo autor não sejam encontrados.
    '''
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