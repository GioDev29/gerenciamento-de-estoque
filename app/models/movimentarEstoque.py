from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class MovimentacaoEstoque(Base):
    __tablename__= "mov_estoque"
    
    id = Column(Integer, primary_key=True)
    tipo = Column(String(7), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo_user = Column(String(10), nullable=False)
    id_user = Column(Integer, nullable=False)
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.now)

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if not valor:
            raise ValueError("O tipo não pode ser vazio.")
        self._tipo = valor
        
    @property
    def tipo_user(self):
        return self._tipo_user

    @tipo_user.setter
    def tipo_user(self, valor):
        if not valor:
            raise ValueError("O usuário não pode ser vazio, informe se você é estoquista, gerente ou vendedor.")
        self._tipo_user = valor
        
    @property
    def id_user(self):
        return self._id_user
    
    @id_user.setter
    def id_user(self, valor):
        if not valor:
            raise ValueError("O seu ID não pode ser vázio.")
        self._id_user = valor
        
    @property
    def quantidade(self):
        return self._quantidade
    
    @quantidade.setter
    def quantidade(self, valor):
        if valor == 0:
            raise ValueError("A quantidade não pode ser menor ou igual a zero.")
        self._quantidade = valor
        
        
  