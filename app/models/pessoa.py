from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from database.conexao import Base
from utils.exceptions import (
    EmailJaExisteException,
    CpfJaExistente,
    SalarioNegativo,
    TelefoneJaExiste,
    GerenteNaoExiste,
    ProdutoNaoEncontrado,
    PrecoNegativo,
    EstoquistaJaExiste,
    EstoquistaNaoExiste,
    IdVazio, 
    
)

class Pessoa(Base):
    __abstract__ = True 

    id = Column(Integer, primary_key=True, index=True)
    _nome = Column("nome", String(100), nullable=False)
    _cpf = Column("cpf", String(14), unique=True, nullable=False)
    _email = Column("email", String(100), unique=True)
    _telefone = Column("telefone", String(20))
    _turno = Column("turno", String(1), nullable=False)
    _salario = Column("salario", Numeric(10,2), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pessoa(nome={self.nome})>"

    
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor:
            raise ValueError("Nome não pode ser vazio.")
        self._nome = valor.lower()

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        if len(valor) != 11:
            raise ValueError("CPF deve ter 11 dígitos.")
        self._cpf = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not valor:
            raise ValueError("E-mail não pode ser vazio.")
        self._email = valor

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, valor):
        if len(valor) < 11:
            raise ValueError("Telefone deve ter 11 dígitos.")
        self._telefone = valor

    @property
    def turno(self):
        return self._turno

    @turno.setter
    def turno(self, valor):
        if valor.upper() not in ["M", "T", "N"]:
            raise ValueError("Turno deve ser M (Manhã), T (Tarde) ou N (Noite)")
        self._turno = valor.upper()

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise ValueError("O salário não pode ser negativo")
        self._salario = valor
