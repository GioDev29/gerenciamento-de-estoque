from database.conexao import SessionLocal, Base, engine
from utils import exceptions
from services import gerente_services
import re

def menu_gerente(bd):

    print('\nEscolha uma opção:')
    print('1. Cadastrar Gerente')
    print('1. Cadastrar Vendedor')
    print('2. Cadastrar Estoquista')
    print('3. Listar Vendedores')
    print('4. Listar Estoquistas\n')
    print('_________________________')
    print('5. Visualizar Estoque Total')
    print('6. Visualizar Produto Especifico')
    print('7. Atualizar estoque (Diminuir quantidade)')
    print('8. Listar produtos com estoque baixo')
    print('9. Sair')
    opcao = input("Digite sua opção: ")
    if opcao == '1':
        gerente_services.GerenteServices.criar_gerente(bd)

def menu_estoquista():
    print('1. Atualizar Informações Pessoais')
    print('2. Visualizar Estoque Total')
    print('3. Visualizar Produto Especifico')
    print('Registrar entradas e saídas de estoque')
    print('5. Listar produtos com estoque baixo')
    print('6. Sair')
    
def menu_vendedor():
    print('1. Atualizar Informações Pessoais')
    print('2. Visualizar Estoque Total')
    print('3. Visualizar Produto Especifico')
    print('Registrar entradas e saídas de estoque')
    print('5. Listar produtos com estoque baixo')
    print('6. Sair')

def main():
    Base.metadata.create_all(engine)
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
            menu_gerente(bd)
            
            
        elif opcao == '2':
            menu_estoquista()
            
        elif opcao == '3':
            menu_vendedor()
            
        elif opcao == '4':
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == '__main__':
    main()
    