from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from database.conexao import Base

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True)
    _nome = Column("nome", String(100), nullable=False)
    descricao = Column(String(200), nullable=True)
    _codigo = Column("codigo", Integer, nullable=False, unique=True)
    _preco_compra = Column("preco_compra", Numeric(10,2), nullable=False)
    _preco_venda = Column("preco_venda", Numeric(10,2), nullable=False)
    
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="produto")
    estoques = relationship("Estoque", back_populates="produto")

    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', codigo={self.codigo}, preco_venda={self.preco_venda})>"

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome do produto não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Código deve ser um número inteiro positivo.")
        self._codigo = valor

    @property
    def preco_compra(self):
        return self._preco_compra

    @preco_compra.setter
    def preco_compra(self, valor):
        if valor < 0:
            raise ValueError("Preço de compra não pode ser negativo.")
        self._preco_compra = valor

    @property
    def preco_venda(self):
        return self._preco_venda

    @preco_venda.setter
    def preco_venda(self, valor):
        if valor < 0:
            raise ValueError("Preço de venda não pode ser negativo.")
        self._preco_venda = valor
