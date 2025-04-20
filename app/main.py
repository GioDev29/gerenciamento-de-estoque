from database import SessionLocal
from services.vendedor_service import VendedorService

def main():
    bd = SessionLocal()
    
    while True:
        print('\nEscolha uma opção:')
        print('1. Visão Gerente')
        print('2. Visão Estoquista')
        print('3. Visão Vendedor')
        print('4. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            ## Da para colocar tipo: Coloque seu email, se esse email existir ai ele tem acesso
            ## A gente pode colocar uma senha especifica para que a gente consiga criar um gestor
            
            
            print('\nEscolha uma opção:')
            print('1. Cadastrar Vendedor')
            print('1. Cadastrar Estoquista')
            print('1. Listar Vendedores')
            print('1. Listar Estoquistas\n')
            print('_________________________')
            print('2. Visualizar Estoque Total')
            print('3. Visualizar Produto Especifico')
            print('4. Atualizar estoque (Diminuir quantidade)')
            print('5. Listar produtos com estoque baixo')
            print('6. Sair')
        elif opcao == '2':
            print('1. Atualizar Informações Pessoais')
            print('2. Visualizar Estoque Total')
            print('3. Visualizar Produto Especifico')
            print('Registrar entradas e saídas de estoque')
            print('5. Listar produtos com estoque baixo')
            print('6. Sair')
        elif opcao == '3':
            print('1. Atualizar Informações Pessoais')
            print('2. Visualizar Estoque Total')
            print('3. Visualizar Produto Especifico')
            print('Registrar entradas e saídas de estoque')
            print('5. Listar produtos com estoque baixo')
            print('6. Sair')
        elif opcao == '5':
            break
        else:
            print('Opção inválida. Tente novamente.')
    
    


if __name__ == '__main__':
    main()
    