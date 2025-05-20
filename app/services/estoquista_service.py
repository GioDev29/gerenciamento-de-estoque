from models.estoquista import Estoquista
from utils.exceptions import (
    EmailJaExisteException,
    CpfJaExistente,
    SalarioNegativo,
    TelefoneJaExiste,
    GerenteNaoExiste,
    ProdutoNaoEncontrado,
    PrecoNegativo
)
import re

class EstoquistaService:
    def __init__(self, bd):
        self._bd = bd  

    def criar_estoquista(self):
        try:
            nome = input("Insira o nome: ")
            cpf = input("Insira o cpf (SOMENTE NÚMEROS): ")
            email = input("Insira o E-mail: ")
            telefone = input("Insira o Telefone: ")
            turno = input("Insira o Turno (M, T, N): ").upper()
            salario = float(input("Insira o Salário: "))

            if salario <= 0:
                raise ValueError("Salário deve ser maior que zero!")
            if turno not in ['M', 'T', 'N']:
                raise ValueError("Turno inválido! Use M, T ou N.")

            estoquista = Estoquista(
                nome=nome,
                cpf=cpf,
                email=email,
                telefone=telefone,
                turno=turno,
                salario=salario
            )

            self._bd.add(estoquista)
            self._bd.commit()
            print("Estoquista cadastrado com sucesso!")

        except ValueError as ve:
            self._bd.rollback()
            print(f"Erro de validação: {ve}")

        except Exception as e:
            self._bd.rollback()
            msg = str(e).lower()
            if "cpf" in msg:
                print("Erro: CPF já cadastrado!")
            elif "telefone" in msg:
                print("Erro: Telefone já cadastrado!")
            elif "email" in msg:
                print("Erro: E-mail já cadastrado!")
            else:
                print(f"Erro inesperado: {e}")

    def listar_estoquistas(self):
        estoquistas = self._bd.query(Estoquista).all()
        for estoquista in estoquistas:
            print(estoquista)

    def listar_estoquista(self):
        cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
        estoquista = self._bd.query(Estoquista).filter_by(cpf=cpf).first()
        if not estoquista:
            print(f'Estoquista com CPF "{cpf}" não encontrado.')
            return
        print(estoquista)
        
    def atualizar_estoquista(self, cpf):
        cpf_limpo = re.sub(r'\D', '', cpf)
        estoquista = self._bd.query(Estoquista).filter_by(cpf=cpf_limpo).first()

        if not estoquista:
            raise ValueError('Pessoa não existe')

        print('O que deseja atualizar?')
        print('1. Nome\n2. E-mail\n3. Telefone\n4. Turno\n5. Nenhuma opção')

        opcao = input('Opção: ')
        if opcao == '1':
            nome = input("Novo nome: ")
            estoquista.nome = nome
        elif opcao == '2':
            email = input("Novo email: ")
            if self._bd.query(Estoquista).filter_by(email=email).first():
                raise EmailJaExisteException(email)
            estoquista.email = email
        elif opcao == '3':
            telefone = input("Novo telefone: ")
            telefone_limpo = re.sub(r'\D', '', telefone)
            if self._bd.query(Estoquista).filter_by(telefone=telefone_limpo).first():
                raise TelefoneJaExiste(telefone_limpo)
            estoquista.telefone = telefone_limpo
        elif opcao == '4':
            turno = input("Novo turno (M, T, N): ").upper()
            if turno not in ['M', 'T', 'N']:
                raise Exception("Turno inválido!")
            estoquista.turno = turno
        elif opcao == '5':
            print("Nenhuma alteração realizada.")
            return
        else:
            print("Opção inválida.")
            return

        self._bd.commit()
        print("Atualização realizada com sucesso.")

    def deletar_estoquista(self):
        try:
            cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
            estoquista = self._bd.query(Estoquista).filter_by(cpf=cpf).first()

            if not estoquista:
                print("O estoquista não existe.")
                return

            confirmacao = input(f"Tem certeza que deseja deletar o estoquista {estoquista.nome}? (S/N): ")

            if confirmacao.upper() != 'S':
                print("Operação cancelada pelo usuário.")
                return

            self._bd.delete(estoquista)
            self._bd.commit()

            print("Estoquista removido com sucesso!")

        except Exception as e:
            self._bd.rollback()
            print(f"Erro inesperado ao deletar: {e}")
