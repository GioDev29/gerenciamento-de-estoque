from .pessoa import Pessoa
from sqlalchemy import Column, String

class Gerente(Pessoa):
    __tablename__ = 'gerentes'
    
    _setor = Column("setor", String(100), nullable=False)

    def __repr__(self):
        return f'<Gerente(id={self.id}, nome={self.nome}, cpf={self.cpf})>'

    @property
    def setor(self):
        return self._setor

    @setor.setter
    def setor(self, valor):
        if not valor:
            raise ValueError("Setor não pode ser vazio.")
        self._setor = valor
