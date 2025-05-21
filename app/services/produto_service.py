from models.produto import Produto
from models.estoque import Estoque
from utils.exceptions import (
    GerenteNaoExiste,
    EmailJaExisteException,
    CpfJaExistente,
    TelefoneJaExiste,
    SalarioNegativo,
    VendedorNaoExiste,
    ProdutoNaoExiste,
    ProdutoJaExiste,
    ErroNaQuantidade
)

class ProdutoService:
    def __init__(self, bd):
        self._bd = bd  

    def criar_produto(self):
        try:
            id = int(input("Insira o ID do produto: "))
            nome = input("Insira o nome do produto: ")
            descricao = input("Insira a descrição do produto: ")
            codigo = int(input("Insira o código do produto: "))
            preco_compra = float(input("Insira o preço de compra do produto: "))
            preco_venda = float(input("Insira o preço de venda do produto: "))

            codigo_existe = self._bd.query(Produto).filter_by(_codigo=codigo).first()
            if codigo_existe:
                raise ProdutoJaExiste(codigo)

            produto = Produto(
                id=id,
                _nome=nome,
                descricao=descricao,
                _codigo=codigo,
                _preco_compra=preco_compra,
                _preco_venda=preco_venda
            )
            self._bd.add(produto)
            self._bd.flush()  

            qtd_inicial = int(input("Qual a quantidade inicial no estoque? "))
            if qtd_inicial < 0:
                raise ErroNaQuantidade(qtd_inicial)

            estoque = Estoque(
                _produto_id=produto.id,
                _quantidade=qtd_inicial
            )
            self._bd.add(estoque)

            self._bd.commit()
            print("Produto e estoque criados com sucesso!")

        except (ProdutoJaExiste, ErroNaQuantidade) as e:
            self._bd.rollback()
            print(e)
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao criar produto: {e}")


    def deletar_produto(self, codigo_barras):
        try:
            produto = self._bd.query(Produto).filter_by(Produto._codigo == codigo_barras).first()
            if produto:
                self._bd.delete(produto)
                self._bd.commit()
                print(f"Produto com Codigo de Barras {codigo_barras} deletado.")
            else:
                raise ProdutoNaoExiste(codigo_barras)
        except ProdutoNaoExiste as p:
            print(p)
            self._bd.rollback()
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao deletar produto: {e}")

    def listar_produtos(self):
        produtos = self._bd.query(Produto).all()
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        for produto in produtos:
            print(produto)

    def listar_produto(self):
        try:
            id = int(input("Digite o ID do produto que deseja ver: "))
            produto = self._bd.query(Produto).filter_by(id=id).first()
            if not produto:
                raise ProdutoNaoExiste(id)
            print(produto)
        except ProdutoNaoExiste as p:
            print(p)
            self._bd.rollback()
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    def modificar_produto(self, produto_id):
        produto = self._bd.query(Produto).filter_by(Produto.id == produto_id).first()
        if not produto:
            raise ProdutoNaoExiste(produto_id)

        print('O que deseja atualizar? ')
        print('------------------------')
        print('\nEscolha uma opção:')
        print('1. ID.')
        print('2. Nome.')
        print('3. Descrição.')
        print('4. Código.')
        print('5. Preço de Compra.')
        print('6. Nenhuma das opções.')
            
        opcao = input('Opção: ')

        if opcao == '1': 
            try:
                id_novo = int(input("Novo ID: "))
                produto.id = id_novo
            except ValueError:
                print("ID inválido. Deve ser um número inteiro.")
                return

        elif opcao == '2':
            nome = input("Novo nome: ")
            produto.nome = nome

        elif opcao == '3':
            descricao = input("Nova descrição: ")
            produto.descricao = descricao

        elif opcao == '4':
            try:
                codigo = int(input("Novo código: "))
                produto.codigo = codigo 
            except ValueError:
                print("Código inválido. Deve ser um número inteiro.")
                return

        elif opcao == '5':
            try:
                preco_compra = float(input("Novo preço de compra: "))
                produto.preco_compra = preco_compra
            except ValueError:
                print("Preço inválido. Deve ser um número decimal.")
                return

        elif opcao == '6':
            print("Nenhuma alteração realizada.")
            return
        
        else:
            print('Opção inválida. Tente novamente.')
            return

        try:
            self._bd.commit()
            print("Produto atualizado com sucesso!")
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao atualizar produto: {e}")
