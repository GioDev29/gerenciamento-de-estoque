import re
from models.estoquista import Estoquista
from models.gerente import Gerente
from models.vendedor import Vendedor
from .gerente_services import GerenteService
from .pessoa_services import CRUDAbstrato
from utils.validacoes import Validacoes
from utils.exceptions import (
    GerenteNaoExiste,
    EmailJaExisteException,
    CpfJaExistente,
    TelefoneJaExiste,
    SalarioNegativo,
    VendedorNaoExiste,
    IdVazio,
    CpfInvalido,
    NomeInvalido,
    EstoquistaJaExiste,
    TelefoneInvalido,
    TurnoInvalido
)

class VendedorService(CRUDAbstrato):
    def __init__(self, bd):
        self._bd = bd  

    
    def criar(self, id_gerente):
        try: 
            print(f"O seu ID {id_gerente} será utilizado para esse Estoquista")
            gerente = self._bd.query(Gerente).filter_by(id=id_gerente).first()
            if not gerente:
                raise GerenteNaoExiste(id_gerente)
            
            if id_gerente == '':
                raise IdVazio(id_gerente)

            nome = input("Insira o nome: ")
            if len(nome) < 3:
                raise NomeInvalido(nome)

            cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
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
            
            turno = input("Insira o o Turno(M, T, N): ").upper()
            if turno not in ['M', 'T', 'N']:
                raise TurnoInvalido(turno)
            
            salario = float(input("Insira o Salário: "))
            if Validacoes.salario_negativo():
                raise SalarioNegativo(salario)
            


            vendedor = Vendedor(
                _nome=nome,
                _cpf=cpf_limpo,
                _email=email,
                _telefone=telefone_limpo,
                _turno=turno,
                _salario=salario,
                gerente_id=id_gerente  
            )

            self._bd.add(vendedor)
            self._bd.commit()
        except (GerenteNaoExiste, EmailJaExisteException, CpfJaExistente, TelefoneJaExiste, SalarioNegativo, NomeInvalido, IdVazio, TelefoneInvalido, CpfInvalido, TurnoInvalido) as e:
            print(e)
            self._bd.rollback()
            return
        except Exception as ex:
            self._bd.rollback()
            return

    def deletar(self):
        cpf = input("Digite o CPF para deletar: ")
        cpf_limpo = GerenteService.validar_cpf(cpf)
        vendedor = self._bd.query(Vendedor).filter_by(_cpf=cpf_limpo).first()
        if vendedor:
            self._bd.delete(vendedor)
            self._bd.commit()
            print(f"Vendedor com CPF {cpf_limpo} deletado.")
        else:
            print("Vendedor não encontrado.")
            
        try:
            cpf = input("Insira o CPF do Vendedor que deseja deletar (SOMENTE NÚMEROS): ")
            cpf_limpo = Validacoes.validar_cpf(cpf)
            vendedor = self._bd.query(Vendedor).filter_by(_cpf=cpf_limpo).first()

            if not vendedor:
                raise VendedorNaoExiste(vendedor)

            confirmacao = input(f"Tem certeza que deseja deletar o vendedor {vendedor._nome}? (S/N): ")

            if confirmacao.upper() != 'S':
                print("Operação cancelada pelo usuário.")
                return

            self._bd.delete(vendedor)
            self._bd.commit()

            print("Vendedor removido com sucesso!")
        except (VendedorNaoExiste, CpfInvalido) as e:
            print(e)
            self._bd.rollback()
            return
        except Exception as e:
            self._bd.rollback()
            print(f"Erro inesperado ao deletar: {e}")
            return

    def listar_tudo(self):
        vendedores = self._bd.query(Vendedor).all()
        if not vendedores:
            print("Não existem vendedores cadastrados no momento.")
            return
        for vendedor in vendedores:
            print(vendedor)

    def listar_vendedor(self):
        cpf = input("Digite o CPF para buscar: ")
        try:
            cpf_limpo = Validacoes.validar_cpf(cpf)
            vendedor = self._bd.query(Vendedor).filter_by(_cpf=cpf_limpo).first()

            if not vendedor:
                raise VendedorNaoExiste(f'Vendedor com CPF "{cpf_limpo}" não foi encontrado.')
            print(vendedor)
        except (VendedorNaoExiste, CpfInvalido) as v:
            print(v)
            return
    
    def listar_dados(self, cpf):
        cpf_limpo = GerenteService.validar_cpf(cpf)
        vendedor = self._bd.query(Vendedor).filter_by(_cpf=cpf_limpo).first()
        if not vendedor:
            print(f'Vendedor com CPF "{cpf_limpo}" não foi encontrado.')
            return
        else:
            print(vendedor)

    def atualizar(self, cpf):
        try: 
            cpf_limpo = GerenteService.validar_cpf(cpf)
            vendedor = self._bd.query(Vendedor).filter_by(_cpf=cpf_limpo).first()

            if not vendedor:
                raise VendedorNaoExiste(cpf_limpo)

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
                vendedor._nome = nome
            elif opcao == '2':
                email = input("Novo email: ")
                if Validacoes.email_ja_existe(self._bd, email):
                    raise EmailJaExisteException(email)
                vendedor._email = email
            elif opcao == '3':
                telefone = input("Novo telefone: ")
                telefone_limpo = Validacoes.validar_telefone(telefone)
                if Validacoes.telefone_ja_existe(self._bd, telefone_limpo):
                    raise TelefoneJaExiste(telefone_limpo)
                vendedor._telefone = telefone_limpo
            elif opcao == '4':
                turno = input("Novo turno (M, T, N): ").upper()
                if turno not in ['M', 'T', 'N']:
                    raise TurnoInvalido(turno)
                vendedor._turno = turno
            elif opcao == '5':
                print("Nenhuma alteração realizada.")
                return
            else:
                print("Opção inválida.")
                return

            self._bd.commit()
            print("Atualização realizada com sucesso.")
        except (VendedorNaoExiste, EmailJaExisteException, TelefoneJaExiste, TurnoInvalido,NomeInvalido) as e:
            self._bd.rollback()
            print(e)
            return
            
        except Exception as ex:
            self._bd.rollback()
            print('Erro de validação - ')
            return
