from pydantic import BaseModel


class ErrorSchema(BaseModel):
    '''Define uma mensagem de erro a ser apresentada
    '''
    message: str
