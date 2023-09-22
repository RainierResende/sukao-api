from urllib.parse import unquote
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from model import Session, Produto
from model.produto import Produto
from model.produto_ingrediente import ProdutoIngrediente
from model.ingrediente import Ingrediente
from logger import logger
from schemas.produto import *
from schemas import *


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação do produto.
    """
    try:
        # Crie o objeto Produto diretamente, associando-o aos ingredientes por meio do relacionamento

        novo_produto = adiciona_produto(form)

        return jsonify({"message": "Produto adicionado com sucesso!", "produto":novo_produto}), 200

    except IntegrityError as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{form.produto}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{form.produto}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """    
    return apresenta_produtos(), 200

@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do nome do produto

    Retorna uma representação dos produtos.
    """
    produto_nome = unquote(unquote(query.produto))
    
    return apresenta_produto(produto_nome), 200

@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.produto))
    
    try:

        return deleta_produto(produto_nome), 200

    except IntegrityError as e:
        session.rollback()
        error_msg = "Erro de integridade ao deletar o produto :/"
        logger.warning(f"Erro ao deletar produto #{produto_nome}, {error_msg}")
        return {"message": error_msg}, 400

    except Exception as e:
        session.rollback()
        error_msg = "Não foi possível deletar o produto :/"
        logger.warning(f"Erro ao deletar produto #{produto_nome}, {error_msg}")
        return {"message": error_msg}, 400

if __name__ == "__main__":
    app.run()
