from .pessoa import Pessoa
from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Estoquista(Pessoa):
    __tablename__= 'estoquistas'
    
    gerente_id = Column(Integer, ForeignKey("gerentes.id"), nullable=False)
    gerente = relationship('Gerente', backref='vendedores')
    
    '''
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    telefone = Column(String(20))
    turno = Column(String(1), nullable=False)
    salario = Column(Numeric(10,2), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    '''
    
    def __repr__(self):
        return f'<Estoquista(nome={self.nome}, turno={self.turno}, cpf={self.cpf}, telefone={self.telefone}, salario={self.salario}, data de entrada={self.data_criacao})>'
    