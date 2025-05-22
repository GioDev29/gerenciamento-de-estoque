from models import Produto, Gerente, Estoque, MovimentacaoEstoque, Estoquista, Vendedor
from utils.exceptions import (
    GerenteNaoExiste,
    EmailJaExisteException,
    CpfJaExistente,
    TelefoneJaExiste,
    SalarioNegativo,
    VendedorNaoExiste,
    ProdutoNaoExiste,
    ProdutoJaExiste,
    ErroNaQuantidade,
    NomeInvalido,
    ValorInvalido,
    TextoInvalido
)

from sqlalchemy import func, extract
from models import Produto, MovimentacaoEstoque

class ProdutoService:
    def __init__(self, bd):
        self._bd = bd
        self.produto_mais_vendido = None  

    def produto_mais_vendido_mes(self):
        try:
            ano = int(input('Digite o ano (ex: 2024): ').strip())
            if len(str(ano)) != 4:
                raise ValueError('O ano precisa ter exatamente 4 dígitos.')

            mes = int(input('Digite o mês (1 - 12): ').strip())
            if mes not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                raise ValueError('O mês precisa ser um número de 1 a 12.')

            if mes < 1 or mes > 12:
                raise ValueError('Mês inválido. Deve estar entre 1 e 12.')

            resultado = (
                self._bd.query(
                    Produto,
                    func.sum(MovimentacaoEstoque._quantidade).label("total_vendido")
                )
                .join(MovimentacaoEstoque)
                .filter(MovimentacaoEstoque._tipo == "SAIDA")
                .filter(extract("month", MovimentacaoEstoque.data) == mes)
                .filter(extract("year", MovimentacaoEstoque.data) == ano)
                .group_by(Produto)
                .order_by(func.sum(MovimentacaoEstoque._quantidade).desc())
                .first()
            )

            if resultado:
                produto, total = resultado
                self.produto_mais_vendido = (produto, total)
                print(f"Produto mais vendido em {mes}/{ano}: {produto._nome} - {total} unidades")
                return
            else:
                print(f"Nenhuma venda encontrada para {mes}/{ano}.")
                return 

        except Exception as e:
            print(f"Erro ao buscar produto mais vendido: {e}")
            return 

    def criar_produto(self):
        try:
            nome = input("Insira o nome do produto: ").strip()
            if len(nome) < 3:
                raise NomeInvalido(nome)
            descricao = input("Insira a descrição do produto: ").strip()
            if len(descricao) < 3:
                raise TextoInvalido(descricao)
            codigo = int(input("Insira o código do produto: "))
            codigo_existe = self._bd.query(Produto).filter_by(_codigo=codigo).first()
            if codigo_existe:
                raise ProdutoJaExiste(codigo)
            preco_compra = float(input("Insira o preço de compra do produto: ").strip().replace(",", "."))
            if preco_compra <= 0:
                raise ValorInvalido(preco_compra)
            preco_venda = float(input("Insira o preço de venda do produto: ").strip().replace(",", "."))
            if preco_compra <= 0:
                raise ValorInvalido(preco_compra)

            produto = Produto( 
                _nome=nome,
                descricao=descricao,
                _codigo=codigo,
                _preco_compra=preco_compra,
                _preco_venda=preco_venda
            )
            self._bd.add(produto)
            self._bd.flush()  

            qtd_inicial = int(input("Qual a quantidade inicial no estoque? ").strip())
            if qtd_inicial < 0:
                raise ErroNaQuantidade(qtd_inicial)

            estoque = Estoque(
                _produto_id=produto.id,
                _quantidade=qtd_inicial
            )
            self._bd.add(estoque)
            print("ESTOQUE")
            self._bd.commit()
            print("Produto e estoque criados com sucesso!")
            return produto
        except (ProdutoJaExiste, ErroNaQuantidade, NomeInvalido, ValorInvalido, TextoInvalido) as e:
            self._bd.rollback()
            print(e)
            return
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao criar produto: {e}")
            return


    def deletar_produto(self, codigo_barras):
        try:
            produto = self._bd.query(Produto).filter_by(_codigo=codigo_barras).first()
            if not produto:
                raise ProdutoNaoExiste(codigo_barras) 

            confirmacao = input(f"Tem certeza que deseja deletar o gerente: {produto._nome}? (S/N): ").strip()

            if confirmacao.upper() != 'S':
                print("Operação cancelada pelo usuário.")
                return
            
            self._bd.delete(produto)
            self._bd.commit()
            print(f"Produto com Codigo de Barras {codigo_barras} deletado.")
        except ProdutoNaoExiste as p:
            print(p)
            self._bd.rollback()
            return
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao deletar produto: {e}")
            return

    def listar_produtos(self):
        produtos = self._bd.query(Produto).all()
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        for produto in produtos:
            print(produto)

    def listar_produto(self):
        try:
            codigo = int(input("Digite o codigo de barras do produto que deseja ver: ").strip())
            produto = self._bd.query(Produto).filter_by(_codigo=codigo).first()
            if not produto:
                raise ProdutoNaoExiste(id)
            print(produto)
        except ProdutoNaoExiste as p:
            print(p)
            self._bd.rollback()
            return
        except Exception as e:
            print(f"Erro: {e}")
            self._bd.rollback()
            return

    def modificar_produto(self, produto_id):
        try:
            produto = self._bd.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ProdutoNaoExiste(produto_id)

            print('O que deseja atualizar? ')
            print('------------------------')
            print('\nEscolha uma opção:')
            print('1. Nome.')
            print('2. Descrição.')
            print('3. Código.')
            print('4. Preço de Compra.')
            print('5. Nenhuma das opções.')
                
            opcao = input('Opção: ')

            if opcao == '1':
                nome = input("Novo nome: ").strip()
                if len(nome) < 3:
                    raise NomeInvalido(nome)
                produto.nome = nome

            elif opcao == '2':
                descricao = input("Nova descrição: ").strip()
                if len(descricao) < 3:
                    raise TextoInvalido(descricao)
                produto.descricao = descricao
            elif opcao == '3':
                codigo = int(input("Novo código: ").strip())
                produto.codigo = codigo 

            elif opcao == '4':
                preco_compra = float(input("Novo preço de compra: ").strip())
                if preco_compra <= 0:
                    raise ValorInvalido(preco_compra)
                produto.preco_compra = preco_compra
                
            elif opcao == '5':
                print("Nenhuma alteração realizada.")
                return
            
            else:
                print('Opção inválida. Tente novamente.')
                return

            self._bd.commit()
            print("Produto atualizado com sucesso!")
        except (NomeInvalido, ValorInvalido) as e:
            print(e)
            self._bd.rollback()
            return
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao atualizar produto: {e}")
            return
