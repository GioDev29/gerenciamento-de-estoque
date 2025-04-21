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
    


'''
Criar Movimentação
Listar todas Movimentações
Modificar Movimentação
Pesquisar Produto

Quando for criar a funcionalidade de criar vendedor é necessário que tenha como ele colocar quem está fazendo a

'''