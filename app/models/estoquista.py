from .pessoa import Pessoa
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Estoquista(Pessoa):
    __tablename__ = 'estoquistas'
    
    gerente_id = Column(Integer, ForeignKey("gerentes.id"), nullable=False)
    gerente = relationship('Gerente', backref='estoquistas')  # <- corrigido aqui

    def __repr__(self):
        return (
            f'<Estoquista(id={self.id}, nome={self.nome}, turno={self.turno}, '
            f'cpf={self.cpf}, telefone={self.telefone}, salario={self.salario}, '
            f'data_criacao={self.data_criacao})>'
        )
