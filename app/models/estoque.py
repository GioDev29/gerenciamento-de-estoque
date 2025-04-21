from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Estoque(Base):
    __tablename__ = "estoque"
    
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey="produtos.id", nullable=False)
    produto = relationship('Produto', backref='estoque')
    quantidade = Column(Integer, nullable=False)


