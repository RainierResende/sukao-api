from pydantic import BaseModel
from typing import List
from model import Session, Produto
from model.ingrediente import Ingrediente
from sqlalchemy.exc import IntegrityError
from logger import logger

class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    codigo: int
    produto: str
    valor: float
    ingredientes_do_produto: str

class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no nome do produto.
    """
    produto: str

class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos: List[ProdutoSchema]

class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado
    """
    id: int
    codigo: int
    produto: str
    valor: float
    ingredientes_do_produto: str

class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    produto: str

session = Session()

def apresenta_produtos():
    """ Retorna uma representação dos produtos com seus ingredientes.
    """
    produtos = session.query(Produto).all()
    produtos_result = []

    for p in produtos:
        ingredientes_do_produto = [i.name for i in p.ingredientes_do_produto]
        produtos_result.append({
            "codigo": p.codigo,
            "produto": p.produto,
            "valor": p.valor,
            "ingredientes_do_produto": ingredientes_do_produto
        })

    return {"produtos": produtos_result}

def apresenta_produto(produto_nome):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    produto = session.query(Produto).filter(Produto.produto.like(f'%{produto_nome}%')).all()
    produto_result = []

    for p in produto:
        ingredientes_do_produto = [i.name for i in p.ingredientes_do_produto]
        produto_result.append({
            "codigo": p.codigo,
            "produto": p.produto,
            "valor": p.valor,
            "ingredientes_do_produto": ingredientes_do_produto
        })
    
    return {"produto": produto_result}

def adiciona_produto(produto):
    """ Adiciona um produto ao banco de dados seguindo o schema definido em ProdutoSchema
    """
    codigo = produto.codigo
    nome_produto = produto.produto
    valor = produto.valor
    ingredientes_nomes = produto.ingredientes_do_produto.split(', ')

    produto_existente = session.query(Produto).filter(Produto.produto==nome_produto).first()
    
    # Checa se o produto existe, caso não exista adiciona à sessão
    if produto_existente: 
        raise IntegrityError('Produto com mesmo nome já existe no banco de dados')
    
    novo_produto = Produto(codigo=codigo, produto=nome_produto, valor=valor, ingredientes_do_produto=[])

    session.add(novo_produto)
    session.flush()

    # Verifica se o ingrediente já existe
    ingredientes = []

    for ingrediente_nome in ingredientes_nomes:
        ingrediente = session.query(Ingrediente).filter(Ingrediente.name==ingrediente_nome).first()
    
        if not ingrediente:
            ingrediente = Ingrediente(name=ingrediente_nome)
        
        ingredientes.append(ingrediente)

    # Associa os ingredientes ao novo_produto 
    novo_produto.ingredientes_do_produto = ingredientes

    session.add(novo_produto)
    session.flush()   

    # Adiciona o ingrediente ao novo produto
    
    novo_produto.ingredientes_do_produto = ingredientes

    session.commit()

    return {'id':novo_produto.id, 'codigo':novo_produto.codigo, 'valor':novo_produto.valor, 'ingredientes_do_produto':[ingrediente.name for ingrediente in novo_produto.ingredientes_do_produto]}

def deleta_produto(produto_nome):
    """ Deleta um produto do banco de dados
    """
    produto = session.query(Produto).filter(Produto.produto.like(f'%{produto_nome}%')).first()

    if produto:
        session.delete(produto)
        session.commit()
        logger.debug(f"Produto #{produto_nome} deletado")

        return {"message": "Produto removido", "produto":produto_nome}
    else:
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #{produto_nome}, {error_msg}")

        return {"message":error_msg}, 404
