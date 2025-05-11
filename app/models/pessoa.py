from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from database.conexao import Base

class Pessoa(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    telefone = Column(String(20))
    turno = Column(String(1), nullable=False)
    salario = Column(Numeric(10,2), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Produto(nome={self.nome})>"