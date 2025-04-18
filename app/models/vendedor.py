from pessoa import Pessoa
from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Vendedor(Base, Pessoa):
    __tablename__= 'vendedores'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    email = Column(String)
    senha = Column(String)
    tipo = Column(String)
    gerente_id = Column(Integer, ForeignKey('gerentes.id'))
    gerente = relationship('Gerente', backref='vendedores')
    
    
'''
Criar Vendedor
Modificar Vendedor
Listar Vendedor
Deletar Vendedor
Pesquisar Vendedor

Quando for criar a funcionalidade de criar vendedor é necessário que tenha como ele colocar qual é o seu gestor e válidar se ele existe no banco de dados para que ele possa ser colocado lá.


'''
    
    