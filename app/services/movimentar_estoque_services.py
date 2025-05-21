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

class MovimentarEstoque:
    def __init__(self, bd):
        self._bd = bd

    def criar_mov_estoque(self):
        try:
            tipo = input("Insira o tipo de entrada (ENTRADA/SAIDA): ").upper()
            produto_id = int(input("Insira o ID do produto: "))
            tipo_user = input("Insira o tipo de usuario (GERENTE, VENDEDOR OU ESTOQUISTA): ").upper()
            id_user = int(input("Insira o seu ID: "))
            adicionar_diminuir = input("Digite 1 se quer diminuir a quantidade ou 2 para adicionar. [1, 2]: ")

            
            produto = self._bd.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ProdutoNaoEncontrado(produto_id)
                
            estoque = self._bd.query(Estoque).filter_by(_produto_id = produto_id).first()

            quantidade = int(input("Digite a quantidade: "))
            if quantidade < 0: 
                raise ErroNaQuantidade(quantidade)

            if adicionar_diminuir == '1':
                if estoque._quantidade < quantidade:
                    print("Erro: quantidade no estoque é menor do que a desejada para remover.")
                    return
                estoque._quantidade -= quantidade
                print(f"Quantidade atual do produto após remoção: {estoque._quantidade}")
            elif adicionar_diminuir == '2':
                estoque._quantidade += quantidade
                print(f"Quantidade atual do produto após adição: {estoque._quantidade}")
            else:
                print("Insira um valor válido (1 para diminuir, 2 para adicionar).")
                return

            if tipo not in ['ENTRADA', 'SAIDA']:
                raise SemMovimentacaoError(tipo)

            if tipo_user not in ['GERENTE', 'VENDEDOR', 'ESTOQUISTA']:
                raise TipoUsuaioError(tipo_user)

            user = None
            if tipo_user == 'GERENTE':
                user = self._bd.query(Gerente).filter_by(id=id_user).first()
            elif tipo_user == 'VENDEDOR':
                user = self._bd.query(Vendedor).filter_by(id=id_user).first()
            elif tipo_user == 'ESTOQUISTA':
                user = self._bd.query(Estoquista).filter_by(id=id_user).first()

            if not user:
                raise UsuarioNaoEncontrado(id_user)

            mov_estoque = MovimentacaoEstoque(
                _tipo=tipo,
                produto_id=produto.id,
                _tipo_user=tipo_user,
                _id_user=id_user,
                _quantidade=quantidade if adicionar_diminuir == '2' else -quantidade
            )

            self._bd.add(mov_estoque)
            self._bd.commit()
            print("Movimentação registrada com sucesso!")

        except (ProdutoNaoEncontrado, SemMovimentacaoError, TipoUsuaioError, UsuarioNaoEncontrado, ErroNaQuantidade) as e:
            self._bd.rollback()
            print(e)
        except Exception as e:
            self._bd.rollback()
            print(f"Erro inesperado: {e}")

    def listar_movs_estoque(self):
        mov_estoque = self._bd.query(MovimentacaoEstoque).all()
        for mov in mov_estoque:
            print(f"ID: {mov.id}, Tipo: {mov.tipo}, Produto: {mov.produto_id}, Quantidade: {mov.qtd}, Data: {mov.data}")

    def listar_mov_estoque(self):
        try:
            tipo = input("Insira se você quer ver as Entradas ou Saidas (Entrada/Saida): ").upper()

            if tipo not in ['ENTRADA', 'SAIDA']:
                raise SemMovimentacaoError(tipo)

            id_prod = int(input("Digite o ID do produto: "))
            produto = self._bd.query(Produto).filter_by(id=id_prod).first()
            if not produto:
                raise ProdutoNaoEncontrado(id_prod)

            mov_estoque = self._bd.query(MovimentacaoEstoque).filter_by(produto_id=id_prod, _tipo=tipo).all()

            if not mov_estoque:
                print(f'A movimentação do tipo {tipo} para o produto {id_prod} não foi encontrada.')
                return
            else:
                for mov in mov_estoque:
                    print(f"ID Movimentação: {mov.id}, Tipo: {mov._tipo}, Quantidade: {mov._quantidade}, Data: {mov.data}")
        except (SemMovimentacaoError, ProdutoNaoEncontrado) as e:
            print(f"Erro: {e}")
        except ValueError:
            print("ID inválido. Insira um número inteiro.")

    def listar_mov_estoque_produto(self):
        try:
            produto_id = int(input("Insira o ID do produto que deseja ver: "))
            mov_estoque = self._bd.query(MovimentacaoEstoque).filter_by(produto_id=produto_id).all()

            if not mov_estoque:
                print(f'Não tem movimentação do produto com o ID {produto_id}')
                return
            else:
                for mov in mov_estoque:
                    print(f"ID: {mov.id}, Tipo: {mov._tipo}, Quantidade: {mov._quantidade}, Data: {mov.data}")
        except ValueError:
            print("ID do produto inválido. Insira um número inteiro.")
