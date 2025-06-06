from models import Produto, Gerente, Estoque, MovimentacaoEstoque, Estoquista, Vendedor
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
    TipoUsuarioError,
    NomeInvalido
)
import re

class EstoqueServices:
    total_produtos = 0
    qtd_minima = 15
    
    def __init__(self, bd):
        self._bd = bd
        self._produtos = []

    def produtos_bd(self):
        produtos = self._bd.query(Produto).all()
        if not produtos:
            print('Não existem produtos cadastrados no momento.')
            return

        for produto in produtos:
            if produto not in self._produtos:
                self._produtos.append(produto)
                EstoqueServices.total_produtos += 1
            else:
                print(f"Produto '{produto._nome}' já está na lista!")


    @property
    def produtos(self):
        return self._produtos
    
    @classmethod
    def mostrar_total_produtos(cls):
        print(f"Total de produtos adicionados: {cls.total_produtos}")
        
    @classmethod
    def listar_estoque_baixo(cls, bd):
        produtos = bd.query(Estoque).filter(Estoque._quantidade <= cls.qtd_minima).all()

        if not produtos:
            print(f"Todos os produtos estão com estoque maior que {cls.qtd_minima}!")
            return

        print("\nProdutos com estoque abaixo do mínimo:")
        for produto in produtos:
            print(f"- {produto.produto._nome} COD_B {produto.produto._codigo} | Quantidade: {produto._quantidade} | Mínimo ideal: {cls.qtd_minima}")

    
    def criar_estoque(self, produto_id):
        try: 
            id_produto_existente = self._bd.query(Produto).filter_by(id=produto_id).first()

            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente._nome} com o ID: {produto_id}, ele será adicionado ao ESTOQUE.")
            else:
                raise ProdutoNaoEncontrado(produto_id)
            
            qtd_prod = int(input('Qual a quantidade atual do produto que deseja adicionar ao Estoque? ').strip())
            if qtd_prod < 0:
                raise ErroNaQuantidade(qtd_prod)

            estoque = Estoque(
                _produto_id=produto_id,
                _quantidade=qtd_prod
            )

            self._bd.add(estoque)
            self._bd.commit()
            print(f"O produto: {id_produto_existente._nome} foi adicionado ao estoque com sucesso!")
        except (ProdutoNaoEncontrado, ErroNaQuantidade) as e:
            self._bd.rollback()
            print(e)
        except Exception as e:
            print(f"Erro: {e}")

    def listar_produtos_estoque(self):
        produtos = self._bd.query(Estoque).all()
        if not produtos:
            print("Nenhum produto cadastrado no estoque.")
            return
        for produto in produtos:
            print(produto)

    def consultar_produto_estoque(self, id_produto):
        try:
            id_produto_existente = self._bd.query(Estoque).filter_by(_produto_id=id_produto).first()
                
            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente.produto._nome} com o ID: {id_produto}.")
            else:
                raise ProdutoNaoEncontrado(id_produto)
        except ProdutoNaoEncontrado as e:
            print(e)
        except Exception as e:
            print(f"{e}")

    def atualizar_produto_estoque(self, id_produto):
        try:
            id_produto_existente = self._bd.query(Estoque).filter_by(_produto_id=id_produto).first()
                
            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente.produto._nome} com o ID: {id_produto}.")
            else:
                raise ProdutoNaoEncontrado(id_produto)
            
            print('O que deseja atualizar? ')
            print('------------------------')
            print('\nEscolha uma opção:')
            print('1. Nome.')
            print('2. Quantidade.')
            
            opcao = input('Opção: ').strip()
            if opcao == '1':
                nome = input("Nome Novo: ").strip()
                if len(nome) < 3:
                    raise NomeInvalido(nome)
                id_produto_existente.produto._nome = nome
                
            elif opcao == '2':
                qtd = int(input("Nova quantidade, INSIRA A QUANTIDADE -TOTAL- NOVA: ").strip())
                if qtd < 0:
                    raise ErroNaQuantidade(qtd)
                
                id_produto_existente._quantidade = qtd
            
            else:
                print('Opção inválida. Tente novamente.')
                return
            
            self._bd.commit()
            print(f"{id_produto_existente.produto._nome} atualizado com sucesso.")
        except (ProdutoNaoEncontrado, ErroNaQuantidade, NomeInvalido) as e:
            self._bd.rollback()
            print(e)
        except Exception as e:
            print(f"Entrada inválida. {e}")

    def deletar_produto(self):
        try:
            id_produto = int(input("Insira o ID do Produto que deseja DELETAR: ").strip())
            id_produto_existente = self._bd.query(Estoque).filter_by(_produto_id=id_produto).first()
                    
            if id_produto_existente:
                print(f"Encontramos o produto: {id_produto_existente.produto._nome} com o ID: {id_produto}.")
            else:
                raise ProdutoNaoEncontrado(id_produto)
                
            self._bd.delete(id_produto_existente)
            self._bd.commit()
            print(f"Produto com ID {id_produto} deletado com sucesso.")
        except ProdutoNaoEncontrado as e:
            self._bd.rollback()
            print(str(e))
        except ValueError:
            print("ID deve ser um número inteiro")
            return
        except Exception as e:
            print(f"ID inválido. Digite um número inteiro. {e}")
