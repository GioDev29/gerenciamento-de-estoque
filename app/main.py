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

def buscar_usuario_por_cpf(bd, tipo_usuario, cpf):
    model = {
        'GERENTE': Gerente,
        'VENDEDOR': Vendedor,
        'ESTOQUISTA': Estoquista
    }[tipo_usuario]
    return bd.query(model).filter_by(_cpf=cpf).first()

def menu_gerente(bd, gerente):
    while True:
        print('\nMenu Gerente:')
        print('\nInformações Gerente ----')
        print('1. Visualizar dados')
        print('2. Atualizar dados')
        
        print('\nInformações dos Vendedores e Estoquistas ----')
        print('3. Cadastrar Vendedor')
        print('4. Cadastrar Estoquista')
        print('5. Listar Vendedores')
        print('6. Listar Estoquistas')
        
        print('\nFuncionalidade dos produtos dos Produtos ----')
        print('7. Adicionar um Novo Produto')
        print('8. Atualizar um Produto Existente')
        print('8. Visualizar Produto Específico')
        print('10. Listar produtos com estoque baixo')
        print('11. Alterar preço de venda do produto')
        
        print('\nFuncionalidades do Estoque ----')
        print('7. Visualizar Todo o Estoque')
        print('9. Atualizar Estoque (Diminuir/Adicionar quantidade)')

        print('0. Sair')

        opcao = input('Escolha: ')
        if opcao == '1':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.listar_dados(gerente._cpf)
        elif opcao == '2':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.atualizar(gerente._cpf)
        elif opcao == '3':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.criar(gerente.id)
        elif opcao == '4':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.criar(gerente.id)
        elif opcao == '5':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.listar_tudo()
        elif opcao == '6':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.listar_tudo()
        elif opcao == '7':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '8':
            produto_id = int(input("ID do produto: "))
            estoque_s = EstoqueServices(bd)
            estoque_s.consultar_produto_estoque(produto_id)
        elif opcao == '9':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '10':
            EstoqueServices.listar_estoque_baixo(bd)
        elif opcao == '11':
            produto_s = ProdutoService(bd)
            produto_s.listar_produtos()
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.alterar_precos()
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')

def menu_estoquista(bd, estoquista):
    while True:
        print('\nMenu Estoquista:')
        print('\nInformações Estoquista ----')
        print('1. Visualizar Informações Pessoais')
        print('2. Atualizar Informações Pessoais')

        print('\nInformações Informações do Estoque e Produtos ----')
        print('3. Visualizar Todo o Estoque')
        print('4. Visualizar Produto Específico')
        print('5. Registrar Entradas e Saídas de Estoque')
        print('6. Listar Produtos com Estoque Baixo')
        print('0. Sair')

        opcao = input('Escolha: ')
        if opcao == '1':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.listar_dados(estoquista._cpf)
        elif opcao == '2':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.atualizar(estoquista._cpf)
        elif opcao == '3':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '4':
            produto_id = int(input("ID do produto: "))
            estoque_s = EstoqueServices(bd)
            estoque_s.consultar_produto_estoque(produto_id)
        elif opcao == '5':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '6':
            EstoqueServices.listar_estoque_baixo(bd)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')

def menu_vendedor(bd, vendedor):
    while True:
        print('\nMenu Vendedor:')
        print('\nInformações do Vendedor ----')
        print('1. Visualizar Informações Pessoais')
        print('2. Atualizar Informações Pessoais')

        print('\nInformações Informações do Estoque e Produtos ----')
        print('3. Visualizar Todo o Estoque')
        print('4. Visualizar Produto Específico')
        print('5. Registrar Entradas e Saídas de Estoque')
        print('6. Listar Produtos com Estoque Baixo')
        print('0. Sair')

        opcao = input('Escolha: \n')
        if opcao == '1':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.listar_vendedor(vendedor._cpf)
        elif opcao == '2':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.atualizar(vendedor._cpf)
        elif opcao == '3':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '4':
            produto_id = int(input("ID do produto: "))
            estoque_s = EstoqueServices(bd)
            estoque_s.consultar_produto_estoque(produto_id)
        elif opcao == '5':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '6':
            EstoqueServices.listar_estoque_baixo(bd)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')

def main():
    Base.metadata.create_all(engine)
    bd = SessionLocal()
    
    gerente_s = gerente_services.GerenteService(bd)
    gerente_s.listar_tudo()

    while True:
        print('\nEscolha sua visão:')
        print('1. Visão Gerente')
        print('2. Visão Estoquista')
        print('3. Visão Vendedor')
        print('4. Sair')

        opcao = input('Opção: ')

        if opcao == '4':
            print('Tchau!')
            break
        
        try: 
            tipo_usuario = None
            if opcao == '1':
                tipo_usuario = 'GERENTE'
                
                opcao_cadastro = input("Gerente já cadastrado? (S/N) ").upper()
                if opcao_cadastro == 'S':
                    pass
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
            elif opcao == '3':
                tipo_usuario = 'VENDEDOR'
            else:
                print('Opção inválida. Tente novamente.')
                continue
            
            while True:
                try:
                    cpf = input(f'Digite o CPF do {tipo_usuario.lower()}: ')
                    cpf_limpo = Validacoes.validar_cpf(cpf)
                    break 
                except CpfInvalido as e:
                    print(e)

            while not Validacoes.cpf_ja_existe(bd, cpf_limpo):
                while True:
                    try:
                        cpf = input(f'Digite o CPF do {tipo_usuario.lower()}: ')
                        cpf_limpo = Validacoes.validar_cpf(cpf)
                        break
                    except CpfInvalido as e:
                        print(e)

            usuario = buscar_usuario_por_cpf(bd, tipo_usuario, cpf)

            if not usuario:
                if tipo_usuario == 'GERENTE':
                    raise GerenteNaoExiste(cpf_limpo)
                elif tipo_usuario == 'ESTOQUISTA':
                    raise EstoquistaNaoExiste(cpf_limpo)
                elif tipo_usuario == 'VENDEDOR':
                    raise VendedorNaoExiste(cpf_limpo)
        except (CpfInvalido, CpfJaExistente, GerenteNaoExiste, VendedorNaoExiste, EstoquistaNaoExiste) as e:
            print(e)
            return
        except (Exception, ValueError) as e:
            print(e)
            return
        
        if tipo_usuario == 'GERENTE':
            menu_gerente(bd, usuario)
        elif tipo_usuario == 'ESTOQUISTA':
            menu_estoquista(bd, usuario)
        elif tipo_usuario == 'VENDEDOR':
            menu_vendedor(bd, usuario)

if __name__ == '__main__':
    main()
    print("Fim do programa")
