from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from model.base import Base

class Ingrediente(Base):
    __tablename__ = 'ingredientes'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Adicione um relacionamento reverso para produtos
    produtos = relationship("Produto", secondary="produto_ingrediente", back_populates="ingredientes_do_produto")

    def __init__(self, name):
        self.name = name
