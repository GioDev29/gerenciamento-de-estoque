from pessoa import Pessoa
from database.conexao import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship





'''
Criar Produto
Modificar Produto
Listar Produto e mostrar id
Deletar Produto
Pesquisar Produto e mostrar id

Quando for criar a funcionalidade de criar produto é necessário que tenha como ele colocar qual é o id do produto e válidar se ele existe no banco de dados para que ele possa ser colocado lá.

'''