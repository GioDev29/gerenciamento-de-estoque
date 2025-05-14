from models.produto import Produto
from utils.exceptions import ProdutoNaoExiste

class ProdutoService:
    
    def criar_produto(cls, bd):
        try:
            id = int(input("Insira o ID do produto: "))
            nome = input("Insira o nome do produto: ")
            descricao = input("Insira a descrição do produto: ")
            codigo = int(input("Insira o código do produto: "))
            preco_compra = float(input("Insira o preço de compra do produto: "))
            preco_venda = float(input("Insira o preço de venda do produto: "))
            
            produto = Produto(id=id,nome=nome,descricao=descricao,codigo=codigo,preco_compra=preco_compra,preco_venda=preco_venda)
            bd.add(produto)
            bd.commit()
        except:
            bd.rollback()
            pass
    
    def deletar_produto(cls, bd, produto_id: int):
        try:
            produto = bd.query(Produto).filter(Produto.id == produto_id).first()
            if produto:
                bd.delete(produto)
                bd.commit()
        except:
            bd.rollback()
    def listar_produtos(cls, bd):
        produtos = bd.query(Produto).all
        for produto in produtos:
            print(produto)
    def listar_produto(cls,id, bd):
        id = int(input())
        produto = bd.query(Produto).filter_by(id=id).first()
        if not produto:
            print(f'O produto do "{id}" não foi  encontrado.')
            return
        else:
            print(produto)
    def modificar_produto(cls, bd, produto_id: int):
        produto = bd.query(Produto).filter(Produto.id == produto_id).first()
        
        if not produto:
            raise ProdutoNaoExiste(produto_id)

        print('O que deseja atualizar? ')
        print('------------------------')
        print('\nEscolha uma opção:')
        print('1. ID.')
        print('2. Nome.')
        print('3. Descrição')
        print('4. Código')
        print('5. Preço de Compra')
        print('6. Preço de Venda')
        print('7. Nenhuma das opções.')
            
        opcao = input('Opção: ')

        if opcao == '1': 
            id = input("ID: ")
            produto.id = id

        elif opcao == '2':
            nome = input("Nome: ")
            produto.nome = nome

        elif opcao == '3':
            descricao = input("Descrição: ")
            produto.descricao = descricao

        elif opcao == '4':
            codigo = input("Código: ")
            produto.codigo = codigo 

        elif opcao == '5':
            preco_compra = input("Preço de compra: ")
            produto.preco_compra = preco_compra

        elif opcao == '6':
            preco_venda = input("Preço de venda: ")
            produto.preco_venda = preco_venda

        elif opcao == '7':
            print("Nenhuma alteração realizada.")
            return
        
        else:
            print('Opção inválida. Tente novamente.')
            return