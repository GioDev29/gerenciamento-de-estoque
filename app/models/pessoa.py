from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from database.conexao import Base


'''
Essa classe pessoa é uma classe abstrata, ela é herdada por Gerente, Vendedor e Estoquista.
Ao usarmos ela, estamos praticando a herança.
Quando usamos o getters e setters aqui, eles são usados pelas classes filhas e se torna um comportamento básico delas. Então, eles são reutilizados sem precisar reescreve-los, praticando o polimorfismo. 
'''

class Pessoa(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    telefone = Column(String(20))
    turno = Column(String(1), nullable=False)
    salario = Column(Numeric(10,2), nullable=False)
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
        if len(valor) > 1:
            raise ValueError("Escreva M, T ou N")
        self._turno = valor
        
    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if len(valor) < 0:
            raise ValueError("O salário não pode ser negativo")
        self._salario = valor