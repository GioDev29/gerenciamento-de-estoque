from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Estoque(Base):
    __tablename__ = "estoques"
    
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    produto = relationship('Produto', back_populates='estoques')
    quantidade = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Estoque(nome={self.produto_id}, prouto={self.produto.nome}, quantidade_atual={self.quantidade})>'
