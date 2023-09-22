from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from model.base import Base

class Produto(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, unique=True, nullable=False)
    produto = Column(String(255), unique=True, nullable=False)
    valor = Column(Float, nullable=False)

    # Relacionamento com a tabela de junção ProdutoIngrediente
    ingredientes_do_produto = relationship("Ingrediente", secondary="produto_ingrediente", back_populates="produtos")

    def __init__(self, codigo, produto, valor, ingredientes_do_produto):
        """
        Cria um Produto

        Arguments:
            codigo: codigo do produto
            produto: nome do produto
            valor: valor do produto
            ingredientes_do_produto: ingredientes do produto
        """
        self.codigo = codigo
        self.produto = produto
        self.valor = valor
        self.ingredientes_do_produto = ingredientes_do_produto