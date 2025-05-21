from .pessoa import Pessoa
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Vendedor(Pessoa):
    __tablename__ = 'vendedores'
    
    gerente_id = Column(Integer, ForeignKey('gerentes.id'))
    gerente = relationship('Gerente', backref='vendedores')

    def __repr__(self):
        return (
            f'\n Vendedor - ID {self.id} || Nome: {self.nome}, Turno: {self.turno}, '
            f'CPF: {self.cpf}, Telefone: {self.telefone}, Salário: {self.salario} ||'
        )
