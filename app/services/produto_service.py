from models import Produto

class ProdutoService:
    @classmethod
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
    @classmethod
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
                try:
                    produto = bd.query(Produto).filter(Produto.id == produto_id).first()
                    if produto:

                        novo_id_str = input(f"Novo ID ({produto.id} - Deixe em branco para manter: ")
                        if novo_id_str:
                            produto.id = int(novo_id_str)

                        novo_nome = input(f"Novo nome ({produto.nome} - Deixe em branco para manter: ")
                        if novo_nome:
                            produto.nome = novo_nome

                        nova_descricao = input(f"Nova descrição ({produto.descricao} - Deixe em branco para manter: ")
                        if nova_descricao:
                            produto.descricao = nova_descricao

                        novo_codigo_str = input(f"Novo código ({produto.codigo} - Deixe em branco para manter: ")
                        if novo_codigo_str:
                            produto.codigo = int(novo_codigo_str)

                        novo_preco_compra_str = input(f"Novo preço de compra ({produto.preco_compra} - Deixe em branco para manter: ")
                        if novo_preco_compra_str:
                            produto.preco_compra = float(novo_preco_compra_str)

                        novo_preco_venda_str = input(f"Novo preço de venda ({produto.preco_venda} - Deixe em branco para manter: ")
                        if novo_preco_venda_str:
                            produto.preco_venda = float(novo_preco_venda_str)

                        bd.commit()
                    else:
                        print(f"Produto com ID {produto_id} não encontrado.")
                except:
                    bd.rollback()