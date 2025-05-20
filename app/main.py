from database.conexao import SessionLocal, Base, engine
from services import gerente_services, vendedor_service, estoquista_service
from services.estoque_service import EstoqueServices  
from services.movimentar_estoque_services import MovimentarEstoque 
from models.gerente import Gerente
from models.vendedor import Vendedor
from models.estoquista import Estoquista

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
        # print('1. Cadastrar Gerente')
        print('2. Cadastrar Vendedor')
        print('3. Cadastrar Estoquista')
        print('4. Listar Vendedores')
        print('5. Listar Estoquistas')
        print('6. Visualizar Todo o Estoque')
        print('7. Visualizar Produto Específico')
        print('8. Atualizar Estoque (Diminuir/Adicionar quantidade)')
        print('9. Listar produtos com estoque baixo')
        print('0. Sair')

        opcao = input('Escolha: ')
        if opcao == '1':
            gerente_s = gerente_services.GerenteService(bd)
            gerente_s.criar_gerente()
        elif opcao == '2':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.criar_vendedor()
        elif opcao == '3':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.criar_estoquista()
        elif opcao == '4':
            vendedor_s = vendedor_service.VendedorService(bd)
            vendedor_s.listar_vendedores()
        elif opcao == '5':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.listar_estoquistas()
        elif opcao == '6':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '7':
            produto_id = int(input("ID do produto: "))
            estoque_s = EstoqueServices(bd)
            estoque_s.consultar_produto_estoque(produto_id)
        elif opcao == '8':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '9':
            EstoqueServices.listar_estoque_baixo(bd)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')

def menu_estoquista(bd, estoquista):
    while True:
        print('\nMenu Estoquista:')
        print('1. Atualizar Informações Pessoais')
        print('2. Visualizar Todo o Estoque')
        print('3. Visualizar Produto Específico')
        print('4. Registrar Entradas e Saídas de Estoque')
        print('5. Listar Produtos com Estoque Baixo')
        print('0. Sair')

        opcao = input('Escolha: ')
        if opcao == '1':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.atualizar_estoquista(estoquista.cpf)
        elif opcao == '2':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '3':
            produto_id = int(input("ID do produto: "))
            estoque_s = EstoqueServices(bd)
            estoque_s.consultar_produto_estoque(produto_id)
        elif opcao == '4':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '5':
            EstoqueServices.listar_estoque_baixo(bd)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')

def menu_vendedor(bd, vendedor):
    while True:
        print('\nMenu Estoquista:')
        print('1. Atualizar Informações Pessoais')
        print('2. Visualizar Todo o Estoque')
        print('3. Visualizar Produto Específico')
        print('4. Registrar Entradas e Saídas de Estoque')
        print('5. Listar Produtos com Estoque Baixo')
        print('0. Sair')

        opcao = input('Escolha: ')
        if opcao == '1':
            estoquista_s = estoquista_service.EstoquistaService(bd)
            estoquista_s.atualizar_estoquista(vendedor.cpf)
        elif opcao == '2':
            estoque_s = EstoqueServices(bd)
            estoque_s.listar_produtos_estoque()
        elif opcao == '3':
            produto_id = int(input("ID do produto: "))
            estoque_s = EstoqueServices(bd)
            estoque_s.consultar_produto_estoque(produto_id)
        elif opcao == '4':
            mov_s = MovimentarEstoque(bd)
            mov_s.criar_mov_estoque()
        elif opcao == '5':
            EstoqueServices.listar_estoque_baixo(bd)
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')

def main():
    Base.metadata.create_all(engine)
    bd = SessionLocal()
    

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

        tipo_usuario = None
        if opcao == '1':
            tipo_usuario = 'GERENTE'
            
            opcao_cadastro = input("Gerente já cadastrado? (S/N) ").upper()
            if opcao_cadastro == 'S':
                pass
            elif opcao_cadastro == 'N':
                gerente_s = gerente_services.GerenteService(bd)
                gerente_s.criar_gerente()
                return
            else:
                raise ValueError('Opção inválida!')
                
        elif opcao == '2':
            tipo_usuario = 'ESTOQUISTA'
        elif opcao == '3':
            tipo_usuario = 'VENDEDOR'
        else:
            print('Opção inválida. Tente novamente.')
            continue
        
        cpf = input(f'Digite o CPF do {tipo_usuario.lower()}: ')
        usuario = buscar_usuario_por_cpf(bd, tipo_usuario, cpf)

        if not usuario:
            print(f'{tipo_usuario.capitalize()} com CPF {cpf} não encontrado.')
            continue

        if tipo_usuario == 'GERENTE':
            menu_gerente(bd, usuario)
        elif tipo_usuario == 'ESTOQUISTA':
            menu_estoquista(bd, usuario)
        elif tipo_usuario == 'VENDEDOR':
            menu_vendedor(bd, usuario)

if __name__ == '__main__':
    main()
    
