from pessoa import Pessoa
from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Estoquista(Base, Pessoa):
    __tablename__= 'estoquistas'
    
    gerente_id = Column(Integer, ForeignKey('gerentes.id'))
    gerente = relationship('Gerente', backref='vendedores')
    
    def __repr__(self):
        return f'<Estoquista(nome={self.nome}, turno={self.turno})>'
    