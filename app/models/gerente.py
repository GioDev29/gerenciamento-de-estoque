from .pessoa import Pessoa
from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Gerente(Pessoa):
    __tablename__= 'gerentes'
    
    setor = Column(String(100), nullable=False)
    
    
    def __repr__(self):
        return f'<Gerente(id={self.id}, nome={self.nome}, cpf={self.cpf})>'







'''
Criar Gerente
Modificar Gerente
Listar Gerentes
Deletar Gerente
Pesquisar Gerente

'''