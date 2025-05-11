from models.gerente import Gerente
from utils.exceptions import EmailJaExisteException, CpfJaExistente, SalarioNegativo, TelefoneJaExiste, GerenteNaoExiste, GerenteNaoExiste
import re

class GerenteServices:

    def criar_gerente(bd):
        nome = input("Insira o nome: ")

        cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
        cpf_limpo = re.sub(r'\D', '', cpf)

        email = input("Insira o E-mail: ")
        telefone = input("Insira o Telefone: ")
        telefone_limpo = re.sub(r'\D', '', telefone)

        turno = input("Insira o Turno (M, T, N): ").upper()
        try:
            salario = float(input("Insira o Salário: "))
        except ValueError:
            raise SalarioNegativo("Digite um valor válido para salário.")

        setor = input("Qual o setor? ")

        email_existente = bd.query(Gerente).filter_by(email=email).first()
        if email_existente:
            raise EmailJaExisteException(email)

        cpf_existente = bd.query(Gerente).filter_by(cpf=cpf_limpo).first()
        if cpf_existente:
            raise CpfJaExistente(cpf_limpo)

        telefone_existente = bd.query(Gerente).filter_by(telefone=telefone_limpo).first()
        if telefone_existente:
            raise TelefoneJaExiste(telefone_limpo)

        if salario < 0:
            raise SalarioNegativo(salario)

        if turno not in ['M', 'T', 'N']:
            raise Exception("Turno inválido! Use apenas: M (Manhã), T (Tarde) ou N (Noite).")

        gerente = Gerente(
            nome=nome,
            cpf=cpf_limpo,
            email=email,
            telefone=telefone_limpo,
            turno=turno,
            salario=salario,
            setor=setor
        )

        bd.add(gerente)
        bd.commit()

        print(f"Gerente {nome} criado com sucesso.")
    
    def listar_gerentes(bd):
        gerentes = bd.query(Gerente).all()
        for gerente in gerentes:
            print(gerente)
            
    def listar_gerente(bd):
        cpf = input("Insira o cpf(Somente números): ")
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        gerente = bd.query(Gerente).filter_by(cpf=cpf_limpo).first()
        if not gerente:
            raise GerenteNaoExiste(gerente)
        else:
            print(gerente)
            
    def atualizar_gerente(bd, cpf):
        cpf_limpo = re.sub(r'\D', '', cpf)
        gerente = bd.query(Gerente).filter_by(cpf=cpf_limpo).first()
        
        if not gerente:
            raise GerenteNaoExiste
        
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
            gerente.nome = nome
            
        elif opcao == '2':
            email = input("Nome: ")
            
            email_existente = bd.query(Gerente).filter_by(email=email).first()
            if email_existente:
                raise EmailJaExisteException(email)
            
            gerente.email = email
         
        elif opcao == '3':
            
            telefone = input("Nome: ")
            telefone_limpo = re.sub(r'\D', '', telefone)
            
            telefone_existente = bd.query(Gerente).filter_by(telefone=telefone_limpo).first()
            if telefone_existente:
                raise TelefoneJaExiste(telefone_limpo)
            
            gerente.telefone = telefone_limpo
            
        elif opcao == '4':
            turno = input("Turno(M, T ou N): ").upper()
            
            if turno not in ['M', 'T', 'N']:
                raise Exception("Turno inválido! Use apenas: M (Manhã), T (Tarde) ou N (Noite).")
            
            gerente.turno = turno
            
        elif opcao == '5':
            print("Nenhuma alteração realizada.")
            return
        
        else:
            print('Opção inválida. Tente novamente.')
            return
        
        bd.commit()
        print("Gerente atualizado com sucesso.")
        
    def deletar_gerente(bd):
        try:
            cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
            cpf_limpo = re.sub(r'\D', '', cpf)
            
            gerente = bd.query(Gerente).filter_by(cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste("O gerente não exite.")
            
            bd.delete(gerente)
            bd.commit()
        except GerenteNaoExiste as e:
            bd.rollback()
            print(str(e))
            
        
        
        

        
    