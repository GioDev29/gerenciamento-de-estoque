from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(200), nullable=True)
    codigo = Column(Integer, nullable=False)
    preco_compra = Column(Numeric(10,2), nullable=False)
    preco_venda = Column(Numeric(10,2), nullable=False)
    estoques = relationship('Estoque', back_populates='produtos')

    
    def __repr__(self):
        return f"<Produto(id = {self.id}, nome={self.nome}, preco_venda={self.preco_venda})>"


'''
Criar Produto
Modificar Produto
Listar Produto e mostrar id
Deletar Produto
Pesquisar Produto e mostrar id

Quando for criar a funcionalidade de criar estoque é necessário que tenha como ele colocar qual é o id do produto e válidar se ele existe no banco de dados para que ele possa ser colocado lá.

'''