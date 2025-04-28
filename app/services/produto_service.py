from app.main import bd
from models import Produto

class ProdutoService:
    @classmethod
    def criar_produto(cls, session: bd):
        try:
            id = int(input("Insira o ID do produto: "))
            nome = input("Insira o nome do produto: ")
            descricao = input("Insira a descrição do produto: ")
            codigo = int(input("Insira o código do produto: "))
            preco_compra = float(input("Insira o preço de compra do produto: "))
            preco_venda = float(input("Insira o preço de venda do produto: "))
            
            produto = Produto(id=id,nome=nome,descricao=descricao,codigo=codigo,preco_compra=preco_compra,preco_venda=preco_venda)
            session.add(produto)
            session.commit()
        except:
            session.rollback()
            pass
    @classmethod
    def deletar_produto(cls, session: bd, produto_id: int):
        try:
            produto = bd.query(Produto).filter(Produto.id == produto_id).first()
            if produto:
                session.delete(produto)
                session.commit()
        except:
            session.rollback()
    def listar_produtos(cls):
        produtos = bd.query(Produto).all
        for produto in produtos:
            print(produto)
    def listar_produto(cls,id):
        id = int(input())
        produto = bd.query(Produto).filter_by(id=id).first()
        if not produto:
            print(f'O produto do "{id}" não foi  encontrado.')
            return
        else:
            print(produto)