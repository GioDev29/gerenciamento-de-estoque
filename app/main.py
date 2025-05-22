from database.conexao import SessionLocal, Base, engine
from services import gerente_services, vendedor_service, estoquista_service
from services.estoque_service import EstoqueServices  
from services.movimentar_estoque_services import MovimentarEstoque 
from services.produto_service import ProdutoService 
from models.gerente import Gerente
from models.vendedor import Vendedor
from models.estoquista import Estoquista
from utils.validacoes import Validacoes
from utils.exceptions import (CpfInvalido, CpfJaExistente, EstoquistaNaoExiste, VendedorNaoExiste, GerenteNaoExiste)
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def buscar_usuario_por_cpf(bd, tipo_usuario, cpf):
    model = {
        'GERENTE': Gerente,
        'VENDEDOR': Vendedor,
        'ESTOQUISTA': Estoquista
    }[tipo_usuario]
    return bd.query(model).filter_by(_cpf=cpf).first()

def menu_gerente_info(bd, gerente):
    limpar_tela()
    while True:
        print('Informações Gerente')
        print('1. Visualizar Dados Pessoais')
        print('2. Atualizar Dados')
        print('3. Visualizar Outros Gestores')
        print('4. Visualizar Equipe')
        print('0. Voltar')
        
        opcao = input('\nEscolha: ')
        if opcao == '1':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.listar_dados(gerente._cpf)
        elif opcao == '2':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.atualizar(gerente._cpf)
        elif opcao == '3':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.listar_tudo()
        elif opcao == '4':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.listar_funcionarios(gerente.id)
        elif opcao == '0':
            return

def menu_gerente_funcionarios(bd, gerente):
    limpar_tela()
    while True:
        print('\nFuncionalidades Vendedores e Estoquistas ----')
        print('1. Cadastrar Vendedor')
        print('2. Cadastrar Estoquista')
        print('3. Listar Vendedores')
        print('4. Listar Estoquistas')
        print('0. Voltar\n')
        
        opcao = input('\nEscolha: ')
        if opcao == '1':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.criar(gerente.id)
        elif opcao == '2':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.criar(gerente.id)
        elif opcao == '3':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.listar_vendedores_gerente(gerente.id)
        elif opcao == '4':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.listar_estoquistas_gerente(gerente.id)
        elif opcao == '0':
            return

def menu_gerente_produtos(bd, gerente):
    limpar_tela()
    while True:
        print('\nSobre Produtos ----')
        print('1. Adicionar um Novo Produto')
        print('2. Atualizar um Produto Existente')
        print('3. Visualizar Todos os Produtos')
        print('4. Visualizar Produto Específico')
        print('5. Listar produtos com estoque baixo')
        print('6. Alterar preço de venda do produto')
        print('7. Produto mais vendido')
        print('0. Voltar\n')
        
        opcao = input('\nEscolha: ')
        
        if opcao == '1':
            produto_s = ProdutoService(bd)
            produto_s.criar_produto()

        elif opcao == '2':
            produto_id = int(input("ID do produto: "))
            produto_s = ProdutoService(bd)
            produto_s.modificar_produto(produto_id)
        elif opcao == '3': 
            produto_s = ProdutoService(bd)
            produto_s.listar_produtos()
            estoque_s = EstoqueServices(bd)
            estoque_s.produtos_bd()
            estoque_s.mostrar_total_produtos()
        elif opcao == '4':
            produto_s = ProdutoService(bd)
            produto_s.listar_produto()
        elif opcao == '5':
            EstoqueServices.listar_estoque_baixo(bd)
        elif opcao == '6':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.alterar_precos()
        elif opcao == '7':
            produto_s = ProdutoService(bd)
            produto_s.produto_mais_vendido_mes()
        elif opcao == '0':
            return
        
def menu_gerente_estoque(bd, gerente):
    limpar_tela()
    while True:
        print('\nFuncionalidades do Estoque ----')
        print('1. Visualizar Todo o Estoque')
        print('2. Registrar Entradas e Saídas de Estoque')
        print('3. Listar todas as Movimentações')
        print('4. Listar todas as Movimentações(ENTRADA ou SAIDA)')
        print('5. Listar movimentações de um produto')
        print('0. Voltar\n')
        
        opcao = input('\nEscolha: ')
        if opcao == '1':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '2':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '3':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_movs_estoque()
        elif opcao == '4':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_mov_estoque()
        elif opcao == '5':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_mov_estoque_produto()
        elif opcao == '0':
            return

def menu_gerente(bd, gerente):
    limpar_tela()
    while True:
        print("="*50)
        print('\t\tMENU GERENTE')
        print("="*50)
        print('1. Informações Gerente')
        print('2. Vendedores e Estoquistas')
        print('3. Produtos')
        print('4. Estoque')
        print('0. Sair')

        opcao = input('\nEscolha: ')
        if opcao == '1':
            menu_gerente_info(bd, gerente)
        elif opcao == '2':
            menu_gerente_funcionarios(bd, gerente)
        elif opcao == '3':
            menu_gerente_produtos(bd, gerente)
        elif opcao == '4':
            menu_gerente_estoque(bd, gerente)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            return


def menu_estoquista_estoque(bd, gerente):
    limpar_tela()
    while True:
        print('\nSobre o Estoque ----')
        print('1. Visualizar Todo o Estoque')
        print('2. Registrar Entradas e Saídas de Estoque')
        print('3. Listar todas as Movimentações')
        print('4. Listar todas as Movimentações(ENTRADA ou SAIDA)')
        print('5. Listar movimentações de um produto')
        print('0. Voltar\n')
        
        opcao = input('\nEscolha: ')
        if opcao == '1':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '2':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '3':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_movs_estoque()
        elif opcao == '4':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_mov_estoque()
        elif opcao == '5':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_mov_estoque_produto()
        elif opcao == '0':
            return

def menu_estoquista_produto(bd, gerente):
    limpar_tela()
    while True:
        print('\nSobre Produtos ----')
        print('1. Adicionar um Novo Produto')
        print('2. Atualizar um Produto Existente')
        print('3. Visualizar Todos os Produtos')
        print('4. Visualizar Produto Específico')
        print('5. Listar produtos com estoque baixo')
        print('6. Produto mais vendido')
        print('0. Voltar\n')
        
        opcao = input('\nEscolha: ')
        if opcao == '1':
            produto_s = ProdutoService(bd)
            produto_s.criar_produto()

        elif opcao == '2':
            try:
                produto_id = int(input("ID do produto: "))
                produto_s = ProdutoService(bd)
                produto_s.modificar_produto(produto_id)
            except Exception as e:
                print(f'Erro: {e}')
                return
            
        elif opcao == '3': 
            produto_s = ProdutoService(bd)
            produto_s.listar_produtos()
            estoque_s = EstoqueServices(bd)
            estoque_s.produtos_bd()
            estoque_s.mostrar_total_produtos()
            
        elif opcao == '4':
            produto_s = ProdutoService(bd)
            produto_s.listar_produto()
            
        elif opcao == '5':
            EstoqueServices.listar_estoque_baixo(bd)
            
        elif opcao == '6':
            produto_s = ProdutoService(bd)
            produto_s.produto_mais_vendido_mes()
            
        elif opcao == '0':
            return
        

def menu_estoquista_info(bd, estoquista):
    limpar_tela()
    while True:
        print('\nInformações do Estoquista')
        print('1. Visualizar Informações Pessoais')
        print('2. Atualizar Informações Pessoais')
        print('3. Equipe')
        print('0. Sair\n')
        
        opcao = input('Escolha: ')
        if opcao == '1':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.listar_dados(estoquista._cpf)
        elif opcao == '2':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.atualizar(estoquista._cpf)
        elif opcao == '3':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.listar_funcionarios(estoquista.gerente_id)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            return 


def menu_estoquista(bd, estoquista):
    limpar_tela()
    while True:
        print("="*50)
        print('\t\tMENU ESTOQUISTA')
        print("="*50)
        print('1. Informações Estoquista')
        print('2. Produtos')
        print('3. Estoque')
        print('0. Sair')

        opcao = input('\nEscolha: ')
        if opcao == '1':
            menu_estoquista_info(bd, estoquista)
        elif opcao == '2':
            menu_estoquista_produto(bd, estoquista)
        elif opcao == '3':
            menu_estoquista_estoque(bd, estoquista)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            return


def menu_vendedor_produto(bd, vendedor):
    limpar_tela()
    while True:
        print('\nSobre os Produtos ----')
        print('1. Atualizar um Produto Existente')
        print('2. Visualizar Todos os Produtos')
        print('3. Visualizar Produto Específico')
        print('4. Listar produtos com estoque baixo')
        print('5. Alterar preço de venda do produto')
        print('6. Produto mais vendido')
        print('0. Voltar\n')
        
        
        opcao = input('\nEscolha: ')

        if opcao == '1':
            try: 
                produto_id = int(input("ID do produto: "))
                produto_s = ProdutoService(bd)
                produto_s.modificar_produto(produto_id)
            except Exception as e:
                print('Erro {e}')
                return
            
        elif opcao == '2': 
            produto_s = ProdutoService(bd)
            produto_s.listar_produtos()
            estoque_s = EstoqueServices(bd)
            estoque_s.produtos_bd()
            estoque_s.mostrar_total_produtos()
            
        elif opcao == '3':
            produto_s = ProdutoService(bd)
            produto_s.listar_produto()
            
        elif opcao == '4':
            EstoqueServices.listar_estoque_baixo(bd)
            
        elif opcao == '5':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.alterar_precos()
            
        elif opcao == '6':
            produto_s = ProdutoService(bd)
            produto_s.produto_mais_vendido_mes()
            
        elif opcao == '0':
            return


def menu_vendedor_estoque(bd, vendedor):
    limpar_tela()
    while True:
        print('\nSobre o Estoque ----')
        print('1. Visualizar Todo o Estoque')
        print('2. Registrar Entradas e Saídas de Estoque')
        print('3. Listar todas as Movimentações')
        print('4. Listar todas as Movimentações(ENTRADA ou SAIDA)')
        print('5. Listar movimentações de um produto')
        print('0. Voltar\n')
        
        opcao = input('\nEscolha: ')
        if opcao == '1':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '2':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '3':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_movs_estoque()
        elif opcao == '4':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_mov_estoque()
        elif opcao == '5':
            mov_s = MovimentarEstoque(bd)
            mov_s.listar_mov_estoque_produto()
        elif opcao == '0':
            return


def menu_vendedor_info(bd, vendedor):
    limpar_tela()
    while True:
        print('\nInformações do vendedor')
        print('1. Visualizar Informações Pessoais')
        print('2. Atualizar Informações Pessoais')
        print('3. Equipe')
        print('0. Sair\n')
        
        opcao = input('Escolha: ')
        if opcao == '1':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.listar_dados(vendedor._cpf)
        elif opcao == '2':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.atualizar(vendedor._cpf)
        elif opcao == '3':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.listar_funcionarios(vendedor.gerente_id)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            return 

def menu_vendedor(bd, vendedor):
    limpar_tela()
    while True:
        print("="*50)
        print('\t\tMENU VENDEDOR')
        print("="*50)
        print('1. Informações Vendedor')
        print('2. Produtos')
        print('3. Estoque')
        print('0. Sair')

        opcao = input('\nEscolha: ')
        if opcao == '1':
            menu_vendedor_info(bd, vendedor)
        elif opcao == '2':
            menu_vendedor_produto(bd, vendedor)
        elif opcao == '3':
            menu_vendedor_estoque(bd, vendedor)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            return

def main():
    Base.metadata.create_all(engine)
    bd = SessionLocal()
    
    while True:
        print("="*50)
        print("Bem-vindo ao Sistema de Estoque da Loja")
        print('\nEscolha sua visão:')
        print('1. Visão Gerente')
        print('2. Visão Estoquista')
        print('3. Visão Vendedor')
        print('4. Sair')
        print("="*50)

        opcao = input('\nOpção: ')
        if opcao == '4':
            print("Até logo :D")

            break
        while opcao == '':
            opcao = input('Opção: ')
        
        try: 
            tipo_usuario = None
            if opcao == '1':
                tipo_usuario = 'GERENTE'
                
                opcao_cadastro = input(f"{tipo_usuario.lower()} já cadastrado? (S/N) ").upper()
                if opcao_cadastro == 'S':
                    cpf = input(f'Digite o CPF do {tipo_usuario.lower()}: ')    
                    cpf_limpo = Validacoes.validar_cpf(cpf)  
                elif opcao_cadastro == 'N':
                    gerente_s = gerente_services.GerenteService(bd)
                    cpf = input(f'Digite o CPF do {tipo_usuario.lower()}: ')
                    cpf_limpo = Validacoes.validar_cpf(cpf)
                    if Validacoes.cpf_ja_existe(bd, cpf_limpo):
                        raise CpfJaExistente(cpf_limpo)
                    gerente_s.criar(cpf)
                    continue
                else:
                    raise ValueError('Opção inválida!')
                    
            elif opcao == '2':
                tipo_usuario = 'ESTOQUISTA'
                opcao_cadastro = input(f"{tipo_usuario.lower()} já cadastrado? (S/N) ").upper()
                if opcao_cadastro == 'S':
                    cpf = input(f'Digite o CPF do {tipo_usuario.lower()}: ')    
                    cpf_limpo = Validacoes.validar_cpf(cpf)  
                elif opcao_cadastro == 'N':
                    print(f'Somente Gerentes podem cadastrar {tipo_usuario.upper()}S')
                    continue
                else:
                    raise ValueError('Opção inválida!')
                
            elif opcao == '3':
                tipo_usuario = 'VENDEDOR'
                opcao_cadastro = input(f"{tipo_usuario.lower()} já cadastrado? (S/N) ").upper()
                if opcao_cadastro == 'S':
                    cpf = input(f'Digite o CPF do {tipo_usuario.lower()}: ')    
                    cpf_limpo = Validacoes.validar_cpf(cpf)  
                elif opcao_cadastro == 'N':
                    print(f'Somente Gerentes podem cadastrar {tipo_usuario.upper()}S')
                    continue
                else:
                    raise ValueError('Opção inválida!')
            else:
                print('Opção inválida. Tente novamente.')
                continue


            usuario = buscar_usuario_por_cpf(bd, tipo_usuario, cpf_limpo)

            if not usuario:
                if tipo_usuario == 'GERENTE':
                    raise GerenteNaoExiste(cpf_limpo)
                elif tipo_usuario == 'ESTOQUISTA':
                    raise EstoquistaNaoExiste(cpf_limpo)
                elif tipo_usuario == 'VENDEDOR':
                    raise VendedorNaoExiste(cpf_limpo)
        except (CpfInvalido, CpfJaExistente, GerenteNaoExiste, VendedorNaoExiste, EstoquistaNaoExiste) as e:
            print(e)
            continue
        except (Exception, ValueError) as e:
            print(e)
            continue
        
        if tipo_usuario == 'GERENTE':
            menu_gerente(bd, usuario)
        elif tipo_usuario == 'ESTOQUISTA':
            menu_estoquista(bd, usuario)
        elif tipo_usuario == 'VENDEDOR':
            menu_vendedor(bd, usuario)

if __name__ == '__main__':
    main()
    print("Fim do programa")
