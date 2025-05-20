from models.produto import Produto
from utils.exceptions import ProdutoNaoExiste

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
            
            produto = Produto(
                id=id,
                nome=nome,
                descricao=descricao,
                codigo=codigo,
                preco_compra=preco_compra,
                preco_venda=preco_venda
            )
            self._bd.add(produto)
            self._bd.commit()
            print("Produto criado com sucesso!")
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao criar produto: {e}")

    def deletar_produto(self, produto_id: int):
        try:
            produto = self._bd.query(Produto).filter(Produto.id == produto_id).first()
            if produto:
                self._bd.delete(produto)
                self._bd.commit()
                print(f"Produto com ID {produto_id} deletado.")
            else:
                print(f"Produto com ID {produto_id} não encontrado.")
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
                print(f'O produto com ID "{id}" não foi encontrado.')
                return
            print(produto)
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    def modificar_produto(self, produto_id: int):
        produto = self._bd.query(Produto).filter(Produto.id == produto_id).first()
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
