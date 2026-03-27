from flask_openapi3 import OpenAPI, Info
from flask import redirect

from routes.book_routes import book_bp
from routes.author_routes import author_bp

info = Info(title='Digilibra API', version='1.0.0')
app = OpenAPI(__name__, info=info)

app.register_api(book_bp)
app.register_api(author_bp)


@app.get('/')
def home():
    '''Redireciona para a documentação interativa da API.
    
    Ao acessar a rota raiz da aplicação, o usuário é automaticamente 
    encaminhado para a interface gráfica do Swagger gerada pelo OpenAPI3.
    '''
    return redirect('/openapi/swagger')
