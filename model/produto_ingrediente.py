from sqlalchemy import Column, Integer, ForeignKey
from model.base import Base

class ProdutoIngrediente(Base):
    __tablename__ = 'produto_ingrediente'

    produto_id = Column(Integer, ForeignKey('produto.id'), primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.id'), primary_key=True)
