from models import Produto, Gerente, Estoque, MovimentacaoEstoque, Estoquista, Vendedor
from utils.validacoes import Validacoes
from .crud_services import CRUDAbstrato
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
    TipoUsuarioError
)

class MovimentarEstoque(CRUDAbstrato):
    def __init__(self, bd):
        self._bd = bd

    def criar(self, produto):
        try:
            tipo = input("Insira o tipo de entrada (ENTRADA/SAIDA): ").strip().upper()
            if tipo not in ['ENTRADA', 'SAIDA']:
                raise SemMovimentacaoError(tipo)
            
            
            tipo_user = input("Insira o tipo de usuario (GERENTE, VENDEDOR OU ESTOQUISTA): ").strip().upper()
            if tipo_user not in ['GERENTE', 'VENDEDOR', 'ESTOQUISTA']:
                raise TipoUsuarioError(tipo_user)
            
            id_user = int(input("Insira o seu ID: ").strip())
            if not Validacoes.buscar_usuario_por_id(self._bd, tipo_user, id_user):
                raise ValueError(f'Não existe um {tipo_user.lower()} com o ID: {id_user}')
              
            estoque = self._bd.query(Estoque).filter_by(_produto_id = produto).first()
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
                produto_id=produto,
                _tipo_user=tipo_user,
                _id_user=id_user,
                _quantidade=quantidade if tipo == 'ENTRADA' else -quantidade
            )

            self._bd.add(mov_estoque)
            self._bd.commit()
            print("Movimentação registrada com sucesso!")

        except (ProdutoNaoEncontrado, SemMovimentacaoError, TipoUsuarioError, UsuarioNaoEncontrado, ErroNaQuantidade) as e:
            self._bd.rollback()
            print(e)
        except Exception as e:
            self._bd.rollback()
            print(f"Erro inesperado: {e}")

    def listar_tudo(self):
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
                print(mov)
        except Exception as e:
            print(f"Erro: {e}")
            
    def atualizar(self, movimentacao_id):
        try:
            movimentacao = self._bd.query(MovimentacaoEstoque).filter_by(id=movimentacao_id).first()

            if not movimentacao:
                print(f"Nenhuma movimentação com ID {movimentacao_id} foi encontrada.")
                return

            estoque = self._bd.query(Estoque).filter_by(produto_id=movimentacao.produto_id).first()
            if not estoque:
                print("Estoque relacionado não encontrado.")
                return

            print('O que deseja atualizar?')
            print('------------------------')
            print('1. Quantidade')
            print('2. Nenhuma das opções')

            opcao = input('Opção: ')

            if opcao == '1':
                nova_qtd = int(input("Nova quantidade: ").strip())
                if nova_qtd <= 0:
                    raise ValueError("A quantidade deve ser positiva.")
                
                diferenca = nova_qtd - movimentacao._quantidade
                if movimentacao._tipo == 'ENTRADA':
                    if estoque._quantidade + diferenca < 0:
                        raise ValueError("Não é possível aplicar essa alteração. Estoque ficaria negativo.")
                    estoque._quantidade += diferenca
                elif movimentacao._tipo == 'SAIDA':
                    if estoque._quantidade - diferenca < 0:
                        raise ValueError("Não é possível aplicar essa alteração. Estoque ficaria negativo.")
                    estoque._quantidade -= diferenca

                movimentacao._quantidade = nova_qtd

            elif opcao == '2':
                print("Nenhuma alteração realizada.")
                return
            
            else:
                print("Opção inválida.")
                return

            self._bd.commit()
            print("Movimentação atualizada com sucesso.")

        except ValueError as e:
            self._bd.rollback()
            print(f"Erro ao atualizar movimentação: {e}")
        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao atualizar movimentação: {e}")




    def deletar(self, id_produto):
        try:
            movimentacoes = self._bd.query(MovimentacaoEstoque).filter_by(produto_id=id_produto).all()

            if not movimentacoes:
                raise ValueError(f'Não há movimentações para o produto com ID {id_produto}.')

            print("\nMovimentações encontradas:")
            for mov in movimentacoes:
                print(f"ID: {mov.id}, Tipo: {mov._tipo}, Quantidade: {mov._quantidade}, Data: {mov._data}")

            id_mov = int(input('\nDigite o ID da movimentação que deseja deletar: ').strip())
            mov_escolhida = self._bd.query(MovimentacaoEstoque).filter_by(id=id_mov).first()

            if not mov_escolhida:
                print(f"Nenhuma movimentação com ID {id_mov} foi encontrada.")
                return

            confirmacao = input(
                f"Tem certeza que deseja deletar a movimentação ID {id_mov}? Isso vai ANULAR a entrada/saída que você fez no sistema. (S/N): ").strip().upper()

            if confirmacao != 'S':
                print("Operação cancelada pelo usuário.")
                return

            estoque = self._bd.query(Estoque).filter_by(_produto_id=mov_escolhida.produto_id).first()
            if not estoque:
                print("Erro: Estoque não encontrado.")
                return

            if mov_escolhida._tipo == 'ENTRADA':
                if estoque._quantidade < mov_escolhida._quantidade:
                    raise ValueError("Não é possível deletar essa movimentação de entrada, pois isso deixaria o estoque negativo.")
                estoque._quantidade -= mov_escolhida._quantidade
            elif mov_escolhida._tipo == 'SAIDA':
                estoque._quantidade += mov_escolhida._quantidade

            self._bd.delete(mov_escolhida)
            self._bd.commit()
            print(f"Movimentação ID {id_mov} deletada com sucesso. Estoque atualizado!")

        except Exception as e:
            self._bd.rollback()
            print(f"Erro ao deletar movimentação: {e}")
