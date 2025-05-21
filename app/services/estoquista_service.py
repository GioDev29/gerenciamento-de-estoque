from models.estoquista import Estoquista
from models.gerente import Gerente
from models.vendedor import Vendedor
from .gerente_services import GerenteService
from utils.validacoes import Validacoes
from .pessoa_services import CRUDAbstrato
from utils.exceptions import (
    EmailJaExisteException,
    CpfJaExistente,
    SalarioNegativo,
    TelefoneJaExiste,
    GerenteNaoExiste,
    ProdutoNaoEncontrado,
    PrecoNegativo,
    EstoquistaJaExiste,
    EstoquistaNaoExiste,
    IdVazio,
    CpfInvalido,
    NomeInvalido,
    TelefoneInvalido,
    TurnoInvalido
)

import re

class EstoquistaService(CRUDAbstrato):
    def __init__(self, bd):
        self._bd = bd  

    def criar(self, id_gerente):
        try:
            print(f"O seu ID {id_gerente} será utilizado para esse Estoquista")
            if id_gerente == '':
                raise IdVazio(id_gerente)
            
            nome = input("Insira o nome: ")
            if len(nome) < 3:
                raise NomeInvalido(nome)
            cpf = input("Insira o cpf (SOMENTE NÚMEROS): ")
            cpf_limpo = Validacoes.validar_cpf(cpf)
            if Validacoes.cpf_ja_existe(self._bd, cpf):
                raise CpfJaExistente(cpf_limpo)
            
            email = input("Insira o E-mail: ")
            if Validacoes.email_ja_existe(self._bd, email):
                raise EmailJaExisteException(email)
            
            telefone = input("Insira o Telefone: ")
            telefone_limpo = Validacoes.validar_telefone(telefone)
            if Validacoes.telefone_ja_existe(self._bd, telefone_limpo):
                raise TelefoneJaExiste(telefone_limpo)
            
            turno = input("Insira o Turno (M, T, N): ").upper()
            if turno not in ['M', 'T', 'N']:
                raise TurnoInvalido(turno)
            salario = float(input("Insira o Salário: "))
            if Validacoes.salario_negativo():
                raise SalarioNegativo(salario)
            
            gerente = self._bd.query(Gerente).filter_by(id=id_gerente).first()
            if not gerente:
                raise GerenteNaoExiste(id_gerente)


            estoquista = Estoquista(
                _nome=nome,
                _cpf=cpf_limpo,
                _email=email,
                _telefone=telefone_limpo,
                _turno=turno,
                _salario=salario,
                gerente_id=id_gerente
            )

            self._bd.add(estoquista)
            self._bd.commit()
            print("Estoquista cadastrado com sucesso!")

        except (GerenteNaoExiste, EstoquistaJaExiste, IdVazio, CpfInvalido, NomeInvalido, CpfJaExistente, TelefoneInvalido, TurnoInvalido) as ve:
            self._bd.rollback()
            print(f"Erro de validação: {ve}")
            return

        except (Exception, ValueError)  as e:
            self._bd.rollback()
            print(f"Erro de validação.")
            return
            

    def listar_tudo(self):
        estoquistas = self._bd.query(Estoquista).all()
        if not estoquistas:
            print("Não existem estoquistas cadastrados no momento.")
            return
        for estoquista in estoquistas:
            print(estoquista)

    def listar_estoquista(self):
        cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
        
        try:
            cpf_limpo = GerenteService.validar_cpf(cpf)
            estoquista = self._bd.query(Estoquista).filter_by(_cpf=cpf_limpo).first()
            if not estoquista:
                raise EstoquistaNaoExiste(cpf_limpo)
            print(estoquista)
        except (EstoquistaNaoExiste, CpfInvalido) as e:
            print(e)
            return
    
    def listar_dados(self, cpf):
        cpf_limpo = GerenteService.validar_cpf(cpf)
        estoquista = self._bd.query(Estoquista).filter_by(_cpf=cpf_limpo).first()
        if not estoquista:
            print(f'Estoquista com CPF "{cpf}" não encontrado.')
            return
        print(estoquista)
        
    def atualizar(self, cpf):
        try:
            cpf_limpo = GerenteService.validar_cpf(cpf)
            estoquista = self._bd.query(Estoquista).filter_by(_cpf=cpf_limpo).first()
            
            if not estoquista:
                raise EstoquistaNaoExiste(estoquista)

            print('O que deseja atualizar?')
            print('------------------------')
            print('1. Nome.')
            print('2. E-mail.')
            print('3. Telefone.')
            print('4. Turno.')
            print('5. Nenhuma das opções.')

            opcao = input('Opção: ')
            if opcao == '1':
                nome = input("Novo nome: ")
                if len(nome) < 3:
                    raise NomeInvalido(nome)
                estoquista.nome = nome
            elif opcao == '2':
                email = input("Novo email: ")
                if Validacoes.email_ja_existe(self._bd, email):
                    raise EmailJaExisteException(email)
                estoquista._email = email
            elif opcao == '3':
                telefone = input("Novo telefone: ")
                telefone_limpo = re.sub(r'\D', '', telefone)
                if Validacoes.telefone_ja_existe(self._bd, telefone_limpo):
                    raise TelefoneJaExiste(telefone_limpo)
                estoquista._telefone = telefone_limpo
            elif opcao == '4':
                turno = input("Novo turno (M, T, N): ").upper()
                if turno not in ['M', 'T', 'N']:
                    raise TurnoInvalido(turno)
                estoquista._turno = turno
            elif opcao == '5':
                print("Nenhuma alteração realizada.")
                return
            else:
                print("Opção inválida.")
                return

            self._bd.commit()
            print("Atualização realizada com sucesso.")
        except (EstoquistaNaoExiste, EmailJaExisteException, TelefoneJaExiste, NomeInvalido, TurnoInvalido) as e:
            self._bd.rollback()
            print(e)
            return
        except Exception as ve:
            self._bd.rollback()
            print('Erro de validação - ')
            return

    def deletar(self):
        try:
            cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
            cpf_limpo = GerenteService.validar_cpf(cpf)
            estoquista = self._bd.query(Estoquista).filter_by(_cpf=cpf_limpo).first()

            if not estoquista:
                raise EstoquistaNaoExiste(estoquista)

            confirmacao = input(f"Tem certeza que deseja deletar o estoquista {estoquista._nome}? (S/N): ")

            if confirmacao.upper() != 'S':
                print("Operação cancelada pelo usuário.")
                return

            self._bd.delete(estoquista)
            self._bd.commit()

            print("Estoquista removido com sucesso!")

        except Exception as e:
            self._bd.rollback()
            print(f"Erro inesperado ao deletar: {e}")
