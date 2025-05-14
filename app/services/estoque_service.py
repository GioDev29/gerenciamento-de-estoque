from models.produto import Produto
from models.gerente import Gerente
from models.vendedor import Vendedor
from models.estoquista import Estoquista
from models.movimentarEstoque import MovimentacaoEstoque
from models.estoque import Estoque
from utils.exceptions import (
    DuplicidadeDeCpf,
    DuplicidadeDeTelefone,
    EmailJaExisteException,
    ProdutoNaoEncontrado,
    UsuarioNaoEncontrado,
    GerenteNaoExiste,
    SalarioNegativo,
    ErroNaQuantidade,
    SemMovimentacaoError,
    TipoUsuaioError
)
import re

class EstoqueServices:
    def __init__(self):
        self.produtos = []
    
    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    @staticmethod
    def criar_estoque(bd):
        '''
            id = Column(Integer, primary_key=True)
            produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
            produto = relationship('Produto', back_populates='estoques')
            quantidade = Column(Integer, nullable=False)
        '''
        
        try: 
            produto_id = int(input("Insira o ID do produto que deseja adicionar: "))

            id_produto_existente = bd.query(Produto).filter_by(id=produto_id).first()
            
            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente.nome} com o ID: {produto_id}, ele será adicionado ao ESTOQUE.")
            else:
                raise ProdutoNaoEncontrado(id_produto_existente)
            
            qtd_prod = int(input('Qual a quantidade atual do produto que deseja adicionar ao Estoque?'))
            if qtd_prod < 0:
                raise ErroNaQuantidade(qtd_prod)
            estoque = Estoque(
                produto_id=produto_id,
                quantidade=qtd_prod
            )

            bd.add(estoque)
            bd.commit()
            print(f"O produto: {id_produto_existente.nome} foi adicionado ao estoque com sucesso!")
        except (ProdutoNaoEncontrado, ErroNaQuantidade) as e:
            bd.rollback()
            print(e)

    @staticmethod
    def listar_produtos_estoque(bd):
        produtos = bd.query(Produto).all()
        for produto in produtos:
            print(produto)
    
    @staticmethod
    def consultar_produto_estoque(bd):
        try:
            id_produto = int(input("Insira o ID do Produto que deseja visualizar: "))
            id_produto_existente = bd.query(Estoque).filter_by(produto_id=id_produto).first()
                
            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente.produto.nome} com o ID: {id_produto}, ele será adicionado ao ESTOQUE.")
            else:
                raise ProdutoNaoEncontrado(id_produto)
        except ProdutoNaoEncontrado as e:
            print(e)
    
    @staticmethod
    def atualizar_produto_estoque(bd, id_produto):
        try:
            id_produto_existente = bd.query(Estoque).filter_by(produto_id=id_produto).first()
                
            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente.produto.nome} com o ID: {id_produto}.")
            else:
                raise ProdutoNaoEncontrado(id_produto)
            
            print('O que deseja atualizar? ')
            print('------------------------')
            print('\nEscolha uma opção:')
            print('1. Nome.')
            print('2. Quantidade.')
            
            opcao = input('Opção: ')
            if opcao == '1':
                nome = input("Nome Novo: ")
                id_produto_existente.produto.nome = nome
                
            elif opcao == '2':
                qtd = int(input("Nova quantidade, INSIRA A QUANTIDADE -TOTAL- NOVA: "))
                if qtd < 0:
                    raise ErroNaQuantidade(qtd)
                
                id_produto_existente.quantidade = qtd
            
            else:
                print('Opção inválida. Tente novamente.')
                return
            
            bd.commit()
            print(f"{id_produto_existente.produto.nome} atualizado com sucesso.")
        except (ProdutoNaoEncontrado, ErroNaQuantidade) as e:
            bd.rollback()
            print(e)
            
    
    @staticmethod
    def deletar_produto(bd):
        id_produto = int(input("Insira o ID do Produto que deseja DELETAR: "))
        try:
            id_produto_existente = bd.query(Estoque).filter_by(produto_id=id_produto).first()
                    
            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente.produto.nome} com o ID: {id_produto}.")
            else:
                raise ProdutoNaoEncontrado(id_produto)
                
            bd.delete(id_produto_existente)
            bd.commit()
        except ProdutoNaoEncontrado as e:
            bd.rollback()
            print(str(e))
            
    
            