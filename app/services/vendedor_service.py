from models.vendedor import Vendedor
from models.gerente import Gerente
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
import re

class VendedorService:
    
    @staticmethod
    def criar_vendedor(bd):
        id_gerente = int(input("Insira o ID do gerente do Vendedor: "))
        id_gerente_existe = bd.query(Gerente).filter_by(id=id_gerente).first()
        if not id_gerente_existe:
            raise GerenteNaoExiste(id_gerente)
        
        nome = input("Insira o nome: ")

        cpf = input("Insira o cpf (SOMENTE NÚMEROS): ")
        cpf_limpo = re.sub(r'\D', '', cpf)

        email = input("Insira o E-mail: ")
        telefone = input("Insira o Telefone: ")
        telefone_limpo = re.sub(r'\D', '', telefone)

        turno = input("Insira o o Turno(M, T, N): ")
        try:
            salario = float(input("Insira o Salário: "))

        except ValueError:
            raise SalarioNegativo("Digite um valor válido para salário.")
        email_existente = bd.query(Vendedor).filter_by(email=email).first()
        if email_existente:
            raise EmailJaExisteException(email)
        cpf_existente = bd.query(Vendedor).filter_by(cpf=cpf_limpo).first()
        if cpf_existente:
            raise CpfJaExistente(cpf_limpo)

        telefone_existente = bd.query(Vendedor).filter_by(telefone=telefone_limpo).first()
        if telefone_existente:
            raise TelefoneJaExiste(telefone_limpo)

        if salario < 0:
            raise SalarioNegativo(salario)
        if turno not in ['M', 'T', 'N']:
            raise Exception("Turno inválido! Use apenas: M (Manhã), T (Tarde) ou N (Noite).")
        vendedor = Vendedor(
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            turno=turno,
            salario=salario,
            gerente_id=id_gerente)
        bd.add(vendedor)
        bd.commit()

    @staticmethod
    def deletar_vendedor(bd):
        cpf = int(input())
        try:
            vendedor = bd.query(Vendedor).filter(cpf=cpf).first()
            if vendedor:
                bd.delete(vendedor)
                bd.commit()
        except:
            bd.rollback()
    
    @staticmethod
    def listar_vendedores(bd):
        vendedores = bd.query(Vendedor).all
        for vendedor in vendedores:
            print(vendedor)
    
    @staticmethod 
    def listar_vendedor(bd):
        cpf = int(input())
        vendedor = bd.query(Vendedor).filter_by(cpf=cpf).first()
        if not vendedor:
            print(f'O vendedor do "{cpf}" não foi  encontrado.')
            return
        else:
            print(vendedor)
            
    @staticmethod
    def atualizar_vendedor(bd, cpf):
        cpf_limpo = re.sub(r'\D', '', cpf)
        vendedor = bd.query(Vendedor).filter_by(cpf=cpf_limpo).first()
        
        if not vendedor:
            raise VendedorNaoExiste(cpf_limpo)
        
        print('O que deseja atualizar? ')
        print('------------------------')
        print('\nEscolha uma opção:')
        print('1. Nome.')
        print('2. E-mail.')
        print('3. Telefone')
        print('4. Turno')
        print('5. Nenhuma das opções.')
        
        opcao = input('Opção: ')
        if opcao == '1':
            nome = input("Nome: ")
            vendedor.nome = nome
            
        elif opcao == '2':
            email = input("Email: ")
            
            email_existente = bd.query(Vendedor).filter_by(email=email).first()
            if email_existente:
                raise EmailJaExisteException(email)
            
            vendedor.email = email
         
        elif opcao == '3':
            
            telefone = input("Telefone: ")
            telefone_limpo = re.sub(r'\D', '', telefone)
            
            telefone_existente = bd.query(Vendedor).filter_by(telefone=telefone_limpo).first()
            if telefone_existente:
                raise TelefoneJaExiste(telefone_limpo)
            
            vendedor.telefone = telefone_limpo
            
        elif opcao == '4':
            turno = input("Turno(M, T ou N): ").upper()
            
            if turno not in ['M', 'T', 'N']:
                raise Exception("Turno inválido! Use apenas: M (Manhã), T (Tarde) ou N (Noite).")
            
            vendedor.turno = turno
            
        elif opcao == '5':
            print("Nenhuma alteração realizada.")
            return
        
        else:
            print('Opção inválida. Tente novamente.')
            return