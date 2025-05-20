from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.conexao import Base

class MovimentacaoEstoque(Base):
    __tablename__ = "mov_estoque"
    
    id = Column(Integer, primary_key=True)
    _tipo = Column("tipo", String(7), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    _tipo_user = Column("tipo_user", String(10), nullable=False)
    _id_user = Column("id_user", Integer, nullable=False)
    _quantidade = Column("quantidade", Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    produto = relationship("Produto", back_populates="movimentacoes")

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if valor.lower() not in ("entrada", "saida"):
            raise ValueError("O tipo deve ser 'entrada' ou 'saida'.")
        self._tipo = valor.lower()

    @property
    def tipo_user(self):
        return self._tipo_user

    @tipo_user.setter
    def tipo_user(self, valor):
        allowed = {"estoquista", "gerente", "vendedor"}
        if valor.lower() not in allowed:
            raise ValueError(f"Tipo do usuário deve ser um desses: {allowed}")
        self._tipo_user = valor.lower()

    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("O ID do usuário deve ser um inteiro positivo.")
        self._id_user = valor

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("A quantidade deve ser um inteiro maior que zero.")
        self._quantidade = valor

    def __repr__(self):
        return (f"<MovimentacaoEstoque(tipo={self.tipo}, produto_id={self.produto_id}, "
                f"tipo_user={self.tipo_user}, id_user={self.id_user}, quantidade={self.quantidade})>")
