from models import Produto, Gerente, Estoque, MovimentacaoEstoque, Estoquista, Vendedor
from utils.validacoes import Validacoes
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
            tipo = input("Insira o tipo de entrada (ENTRADA/SAIDA): ").strip().upper()
            if tipo not in ['ENTRADA', 'SAIDA']:
                raise SemMovimentacaoError(tipo)
            
            produto_id = int(input("Insira o ID do produto: ").strip())
            produto = self._bd.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ProdutoNaoEncontrado(produto_id)
            
            tipo_user = input("Insira o tipo de usuario (GERENTE, VENDEDOR OU ESTOQUISTA): ").strip().upper()
            if tipo_user not in ['GERENTE', 'VENDEDOR', 'ESTOQUISTA']:
                raise TipoUsuaioError(tipo_user)
            
            id_user = int(input("Insira o seu ID: ").strip())
            if not Validacoes.buscar_usuario_por_id(self._bd, tipo_user, id_user):
                raise ValueError(f'Não existe um {tipo_user.lower()} com o ID: {id_user}')
              
            estoque = self._bd.query(Estoque).filter_by(_produto_id = produto_id).first()
            if not estoque:
                raise ValueError('Esse produto não existe no estoque.')
            quantidade = int(input("Digite a quantidade: ").strip())
            if quantidade < 0: 
                raise ErroNaQuantidade(quantidade)

            if tipo == 'SAIDA':
                if estoque._quantidade < quantidade:
                    raise ValueError(f"A quantidade desse produto é insuficiente. Quantidade: {estoque._quantidade}")
                estoque._quantidade -= quantidade
                print(f"Quantidade atual do produto após remoção: {estoque._quantidade}")
            elif tipo == 'ENTRADA':
                estoque._quantidade += quantidade
                print(f"Quantidade atual do produto após adição: {estoque._quantidade}")
            else:
                raise ValueError("Insira um valor válido (1 para diminuir, 2 para adicionar).")

            mov_estoque = MovimentacaoEstoque(
                _tipo=tipo,
                produto_id=produto.id,
                _tipo_user=tipo_user,
                _id_user=id_user,
                _quantidade=quantidade if tipo == 'ENTRADA' else -quantidade
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
            print(f"{mov.produto._nome.upper()} - ID {mov.produto_id}|| ID Movimentação: {mov.id}, Tipo: {mov._tipo} , Quantidade: {mov._quantidade}, Data: {mov.data}")

    def listar_mov_estoque(self):
        try:
            tipo = input("Insira se você quer ver as Entradas ou Saidas (Entrada/Saida): ").strip().upper()
            if tipo not in ['ENTRADA', 'SAIDA']:
                raise SemMovimentacaoError(tipo)

            id_prod = int(input("Digite o ID do produto: ").strip())
            produto = self._bd.query(Produto).filter_by(id=id_prod).first()
            if not produto:
                raise ProdutoNaoEncontrado(id_prod)

            mov_estoque = self._bd.query(MovimentacaoEstoque).filter_by(produto_id=id_prod, _tipo=tipo).all()

            if not mov_estoque:
                raise ValueError(f'A movimentação do tipo {tipo} para o produto {id_prod} não foi encontrada.')
                return
            else:
                for mov in mov_estoque:
                    print(f"ID Movimentação: {mov.id}, Tipo: {mov._tipo}, Quantidade: {mov._quantidade}, Data: {mov.data}")
        except (SemMovimentacaoError, ProdutoNaoEncontrado) as e:
            print(f"Erro: {e}")
            return
        except Exception as e:
            print(f"Erro: {e}")
            return

    def listar_mov_estoque_produto(self):
        try:
            produto_id = int(input("Insira o ID do produto que deseja ver: ").strip())
            mov_estoque = self._bd.query(MovimentacaoEstoque).filter_by(produto_id=produto_id).all()

            if not mov_estoque:
                raise ValueError(f'Não tem movimentação do produto com o ID {produto_id}')
            
            for mov in mov_estoque:
                print(f"ID: {mov.id}, Tipo: {mov._tipo}, Quantidade: {mov._quantidade}, Data: {mov.data}")
        except Exception as e:
            print(f"Erro: {e}")
