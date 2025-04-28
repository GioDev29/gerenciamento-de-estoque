from pessoa import Pessoa
from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Gerente(Base, Pessoa):
    __tablename__= 'gerentes'
    
    setor = Column(String(100), nullable=False)
    
    
    def __repr__(self):
        return f'<Gerente(nome={self.nome})>'







'''
Criar Gerente
Modificar Gerente
Listar Gerentes
Deletar Gerente
Pesquisar Gerente

'''