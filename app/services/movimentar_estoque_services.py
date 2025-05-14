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
    
    
    
    '''
    Esses métodos que coloquei não necessitam de uma instancia da classe.
    '''
    
    @staticmethod
    def criar_mov_estoque(bd):
        try:
            tipo = input("Insira o tipo de entrada (ENTRADA/SAIDA): ").upper()
            produto_id = int(input("Insira o ID do produto: "))
            tipo_user = input("Insira o tipo de usuario (GERENTE, VENDEDOR OU ESTOQUISTA): ").upper()
            id_user = int(input("Insira o seu ID: "))
            adicionar_diminuir = input("Digite 1 se quer diminuir a quantidade ou 2 para adicionar. [1, 2]: ")

            produto = bd.query(Produto).filter_by(id=produto_id).first()  # Corrigido para Produto
            if not produto:
                print("Produto não encontrado.")
                return

            try:
                quantidade = int(input("Digite a quantidade: "))
            except ValueError:
                print("Quantidade inválida. Digite um número inteiro.")
                return

            if quantidade <= 0:
                print("A quantidade deve ser maior que zero.")
                return

            if adicionar_diminuir == '1':
                if produto.quantidade < quantidade:
                    print("Erro: quantidade no estoque é menor do que a desejada para remover.")
                    return
                produto.quantidade -= quantidade
                print(f"Quantidade atual do produto após remoção: {produto.quantidade}")
            elif adicionar_diminuir == '2':
                produto.quantidade += quantidade
                print(f"Quantidade atual do produto após adição: {produto.quantidade}")
            else:
                print("Insira um valor válido (1 para diminuir, 2 para adicionar).")
                return

            if tipo not in ['ENTRADA', 'SAIDA']:
                raise SemMovimentacaoError(tipo)

            if tipo_user not in ['GERENTE', 'VENDEDOR', 'ESTOQUISTA']:
                raise TipoUsuaioError(tipo_user)

            # Checa o tipo de usuário
            user = None
            if tipo_user == 'GERENTE':
                user = bd.query(Gerente).filter_by(id=id_user).first()
            elif tipo_user == 'VENDEDOR':
                user = bd.query(Vendedor).filter_by(id=id_user).first()
            elif tipo_user == 'ESTOQUISTA':
                user = bd.query(Estoquista).filter_by(id=id_user).first()

            if not user:
                raise UsuarioNaoEncontrado(id_user)

            mov_estoque = MovimentacaoEstoque(
                tipo=tipo,
                produto_id=produto.id,
                tipo_user=tipo_user,
                id_user=id_user,
                qtd=quantidade if adicionar_diminuir == '2' else -quantidade
            )

            bd.add(mov_estoque)
            bd.commit()
            print("Movimentação registrada com sucesso!")

        except (ProdutoNaoEncontrado, SemMovimentacaoError, TipoUsuaioError, UsuarioNaoEncontrado, ErroNaQuantidade) as e:
            bd.rollback()
            print(f"Erro: {e}")
        except Exception as e:
            bd.rollback()
            print(f"Erro inesperado: {e}")
    
    @staticmethod
    def listar_movs_estoque(bd):
        mov_estoque = bd.query(MovimentacaoEstoque).all()  # Corrigido o método .all()
        for mov in mov_estoque:
            print(f"ID: {mov.id}, Tipo: {mov.tipo}, Produto: {mov.produto_id}, Quantidade: {mov.qtd}, Data: {mov.data}")

    @staticmethod
    def listar_mov_estoque(bd):
        tipo = input("Insira se você quer ver as Entradas ou Saidas (Entrada/Saida): ").upper()
        
        if tipo not in ['ENTRADA', 'SAIDA']:
            raise SemMovimentacaoError(tipo)
        
        id_prod = int(input("Digite o ID do produto: "))
        produto = bd.query(Produto).filter_by(id=id_prod).first()
        if not produto:
            raise ProdutoNaoEncontrado(id_prod)
        
        mov_estoque = bd.query(MovimentacaoEstoque).filter_by(produto_id=id_prod, tipo=tipo).all()  # Corrigido o método .all()
        
        if not mov_estoque:
            print(f'A movimentação do tipo {tipo} para o produto {id_prod} não foi encontrada.')
            return
        else:
            for mov in mov_estoque:
                print(f"ID Movimentação: {mov.id}, Tipo: {mov.tipo}, Quantidade: {mov.qtd}, Data: {mov.data}")

    @staticmethod
    def listar_mov_estoque_produto(bd):
        try:
            produto_id = int(input("Insira o ID do produto que deseja ver: "))  # Corrigido para int
            mov_estoque = bd.query(MovimentacaoEstoque).filter_by(produto_id=produto_id).all()  # Corrigido o método .all()
            
            if not mov_estoque:
                print(f'Não tem movimentação do produto com o ID {produto_id}')
                return
            else:
                for mov in mov_estoque:
                    print(f"ID: {mov.id}, Tipo: {mov.tipo}, Quantidade: {mov.qtd}, Data: {mov.data}")
        except ValueError:
            print("ID do produto inválido. Insira um número inteiro.")
