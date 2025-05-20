from database.conexao import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Estoque(Base):
    __tablename__ = "estoques"
    
    id = Column(Integer, primary_key=True)
    _produto_id = Column("produto_id", Integer, ForeignKey("produtos.id"), nullable=False)
    produto = relationship('Produto', back_populates='estoques')
    _quantidade = Column("quantidade", Integer, nullable=False)

    def __repr__(self):
        return f'<Estoque(produto_id={self.produto_id}, produto_nome={self.produto.nome}, quantidade_atual={self.quantidade})>'

    @property
    def produto_id(self):
        return self._produto_id
    
    @produto_id.setter
    def produto_id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("produto_id deve ser um número inteiro positivo.")
        self._produto_id = valor

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("Quantidade deve ser um número inteiro maior ou igual a zero.")
        self._quantidade = valor
