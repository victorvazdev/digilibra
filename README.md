# 📚 Digilibra API - API de Gerenciamento de Biblioteca

Uma API RESTful desenvolvida em Python para o gerenciamento de livros e autores. Este projeto permite o cadastro, consulta, atualização e remoção de registros do acervo de uma biblioteca, garantindo a integridade dos dados através de um banco de dados relacional.

A documentação interativa da API foi construída utilizando o padrão OpenAPI (Swagger), facilitando o teste e a integração das rotas.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** Flask
* **Documentação da API:** Flask-OpenAPI3 (Swagger UI)
* **ORM e Banco de Dados:** SQLAlchemy (SQLite)
* **Validação de Dados:** Pydantic

## 🚀 Como executar o projeto localmente

Siga as instruções abaixo para configurar o ambiente de desenvolvimento e rodar a aplicação na sua máquina.

### Pré-requisitos

Certifique-se de ter o **Python 3.14.3** instalado no seu sistema. Você pode verificar sua versão rodando o seguinte comando no terminal:

```bash
python --version
```

### Passo a passo da Instalação
1. Clone o repositório
(Se o seu projeto estiver no GitHub, coloque o link aqui. Se não, pule esta etapa ou deixe apenas a instrução de navegar até a pasta)

```bash
git clone https://github.com/victorvazdev/digilibra_api
cd digilibra_api
```

2. Crie um Ambiente Virtual (Recomendado)
O ambiente virtual isola as dependências deste projeto das demais instaladas no seu computador.

```bash
# No Windows:
python -m venv venv

# No macOS/Linux:
python3 -m venv venv
````

3. Ative o Ambiente Virtual

```bash
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
```

4. Instale as dependências
Com o ambiente ativado, instale as bibliotecas necessárias listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

## ⚙️ Inicializando a Aplicação
Após configurar o ambiente e instalar as dependências, você pode iniciar o servidor de desenvolvimento do Flask com o seguinte comando:

```bash
flask run --host 0.0.0.0 --port 8000
```

O servidor será iniciado localmente.

### 📖 Acessando a Documentação (Swagger)
Para testar as rotas e ver a documentação interativa, abra o seu navegador e acesse:

👉 http://localhost:8000/openapi/swagger

## 📁 Estrutura do Projeto

* `app.py`: Ponto de entrada da aplicação, onde o servidor é inicializado.
* `/models`: Contém as classes de mapeamento objeto-relacional (ORM) do SQLAlchemy (Ex: Book, Author).
* `/schemas`: Contém as classes do Pydantic responsáveis pela validação dos dados de entrada e saída.
* `/routes`: Contém os Blueprints que separam as rotas por domínio.
