import re
from models.vendedor import Vendedor
from models.gerente import Gerente
from utils.exceptions import (
    GerenteNaoExiste,
    EmailJaExisteException,
    CpfJaExistente,
    TelefoneJaExiste,
    SalarioNegativo,
    VendedorNaoExiste
)

class VendedorService:
    def __init__(self, bd):
        self._bd = bd  

    
    def criar_vendedor(self):
        id_gerente = int(input("Insira o ID do gerente do Vendedor: "))
        gerente = self._bd.query(Gerente).filter_by(id=id_gerente).first()
        if not gerente:
            raise GerenteNaoExiste(id_gerente)

        nome = input("Insira o nome: ")

        cpf = input("Insira o cpf (SOMENTE NÚMEROS): ")
        cpf_limpo = re.sub(r'\D', '', cpf)

        email = input("Insira o E-mail: ")
        telefone = input("Insira o Telefone: ")
        telefone_limpo = re.sub(r'\D', '', telefone)

        turno = input("Insira o o Turno(M, T, N): ").upper()
        try:
            salario = float(input("Insira o Salário: "))
        except ValueError:
            raise SalarioNegativo("Digite um valor válido para salário.")

        if self._bd.query(Vendedor).filter_by(email=email).first():
            raise EmailJaExisteException(email)
        if self._bd.query(Vendedor).filter_by(cpf=cpf_limpo).first():
            raise CpfJaExistente(cpf_limpo)
        if self._bd.query(Vendedor).filter_by(telefone=telefone_limpo).first():
            raise TelefoneJaExiste(telefone_limpo)
        if salario < 0:
            raise SalarioNegativo(salario)
        if turno not in ['M', 'T', 'N']:
            raise Exception("Turno inválido! Use apenas: M (Manhã), T (Tarde) ou N (Noite).")

        vendedor = Vendedor(
            nome=nome,
            cpf=cpf_limpo,
            email=email,
            telefone=telefone_limpo,
            turno=turno,
            salario=salario,
            gerente_id=id_gerente  # associação: vendedor sabe qual gerente gerencia ele
        )

        self._bd.add(vendedor)
        self._bd.commit()

    def deletar_vendedor(self):
        cpf = input("Digite o CPF para deletar: ")
        cpf_limpo = re.sub(r'\D', '', cpf)
        vendedor = self._bd.query(Vendedor).filter_by(cpf=cpf_limpo).first()
        if vendedor:
            self._bd.delete(vendedor)
            self._bd.commit()
            print(f"Vendedor com CPF {cpf_limpo} deletado.")
        else:
            print("Vendedor não encontrado.")

    def listar_vendedores(self):
        vendedores = self._bd.query(Vendedor).all()
        for vendedor in vendedores:
            print(vendedor)

    def listar_vendedor(self):
        cpf = input("Digite o CPF para buscar: ")
        cpf_limpo = re.sub(r'\D', '', cpf)
        vendedor = self._bd.query(Vendedor).filter_by(cpf=cpf_limpo).first()
        if not vendedor:
            print(f'Vendedor com CPF "{cpf_limpo}" não foi encontrado.')
        else:
            print(vendedor)

    def atualizar_vendedor(self, cpf):
        cpf_limpo = re.sub(r'\D', '', cpf)
        vendedor = self._bd.query(Vendedor).filter_by(cpf=cpf_limpo).first()

        if not vendedor:
            raise VendedorNaoExiste(cpf_limpo)

        print('O que deseja atualizar?')
        print('1. Nome\n2. E-mail\n3. Telefone\n4. Turno\n5. Nenhuma opção')

        opcao = input('Opção: ')
        if opcao == '1':
            nome = input("Novo nome: ")
            vendedor.nome = nome
        elif opcao == '2':
            email = input("Novo email: ")
            if self._bd.query(Vendedor).filter_by(email=email).first():
                raise EmailJaExisteException(email)
            vendedor.email = email
        elif opcao == '3':
            telefone = input("Novo telefone: ")
            telefone_limpo = re.sub(r'\D', '', telefone)
            if self._bd.query(Vendedor).filter_by(telefone=telefone_limpo).first():
                raise TelefoneJaExiste(telefone_limpo)
            vendedor.telefone = telefone_limpo
        elif opcao == '4':
            turno = input("Novo turno (M, T, N): ").upper()
            if turno not in ['M', 'T', 'N']:
                raise Exception("Turno inválido!")
            vendedor.turno = turno
        elif opcao == '5':
            print("Nenhuma alteração realizada.")
            return
        else:
            print("Opção inválida.")
            return

        self._bd.commit()
        print("Atualização realizada com sucesso.")
