from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class Author(Base):
    '''Representa um autor no sistema.

    Esta entidade mapeia a tabela 'author' no banco de dados e gerencia os dados 
    referentes aos criadores das obras. Possui um relacionamento de um-para-muitos (1:N) 
    com a entidade Book, permitindo acessar todos os livros vinculados a um determinado autor
    através da propriedade 'books'.
    '''
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    books = relationship('Book', back_populates='author_rel')

    def __init__(self, name: str):
        '''Inicializa um novo registro de autor.

        Argumentos:
            name (str): Nome completo ou artístico do autor.
        '''
        self.name = name
