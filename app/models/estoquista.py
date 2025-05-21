from .pessoa import Pessoa
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Estoquista(Pessoa):
    __tablename__ = 'estoquistas'
    
    gerente_id = Column(Integer, ForeignKey("gerentes.id"), nullable=False)
    gerente = relationship('Gerente', backref='estoquistas')  # <- corrigido aqui

    def __repr__(self):
        return (
            f'\nEstoquista - ID {self.id} || Nome: {self.nome}, Turno: {self.turno}, '
            f'CPF: {self.cpf}, Telefone: {self.telefone}, Salário: {self.salario} ||'
        )
