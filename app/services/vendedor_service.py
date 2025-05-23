import re
from models import Produto, Gerente, Estoque, MovimentacaoEstoque, Estoquista, Vendedor
from .gerente_services import GerenteService
from .crud_services import CRUDAbstrato
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
    TurnoInvalido,
    EmailInvalido
)

class VendedorService(CRUDAbstrato):
    def __init__(self, bd):
        self._bd = bd  

    
    def criar(self, id_gerente):
        try: 
            if id_gerente == '':
                raise IdVazio(id_gerente)
            gerente = self._bd.query(Gerente).filter_by(id=id_gerente).first()
            if not gerente:
                raise GerenteNaoExiste(id_gerente)
            print(f"O seu ID {id_gerente} será utilizado para esse Estoquista")

            nome = input("Insira o nome: ").strip()
            if len(nome) < 3:
                raise NomeInvalido(nome)

            cpf = input("Insira o CPF (SOMENTE NÚMEROS): ").strip()
            cpf_limpo = Validacoes.validar_cpf(cpf)
            if Validacoes.cpf_ja_existe(self._bd, cpf):
                raise CpfJaExistente(cpf_limpo)
            
            email = input("Insira o E-mail: ").strip()
            email_limpo = Validacoes.validar_email(email)
            if Validacoes.email_ja_existe(self._bd, email):
                raise EmailJaExisteException(email)
            
            telefone = input("Insira o Telefone: ").strip()
            telefone_limpo = Validacoes.validar_telefone(telefone)
            if Validacoes.telefone_ja_existe(self._bd, telefone_limpo):
                raise TelefoneJaExiste(telefone_limpo)
            
            turno = input("Insira o o Turno(M, T, N): ").strip().upper()
            if turno not in ['M', 'T', 'N']:
                raise TurnoInvalido(turno)
            
            salario = float(input("Insira o Salário: ").strip().replace(",", "."))
            if Validacoes.salario_negativo(salario):
                raise SalarioNegativo(salario)
            


            vendedor = Vendedor(
                _nome=nome,
                _cpf=cpf_limpo,
                _email=email_limpo,
                _telefone=telefone_limpo,
                _turno=turno,
                _salario=salario,
                gerente_id=id_gerente  
            )

            self._bd.add(vendedor)
            self._bd.commit()
            print(f'Vendedor: {nome} criado com sucesso!')
        except (GerenteNaoExiste, EmailJaExisteException, CpfJaExistente, TelefoneJaExiste, SalarioNegativo, NomeInvalido, IdVazio, TelefoneInvalido, CpfInvalido, TurnoInvalido, EmailInvalido, SalarioNegativo) as e:
            print(e)
            self._bd.rollback()
            return
        except Exception as ex:
            print(f'Erro: {ex}')
            self._bd.rollback()
            return

    def deletar(self):
        try:
            cpf = input("Insira o CPF do Vendedor que deseja deletar (SOMENTE NÚMEROS): ").strip()
            cpf_limpo = Validacoes.validar_cpf(cpf)
            vendedor = self._bd.query(Vendedor).filter_by(_cpf=cpf_limpo).first()

            if not vendedor:
                raise VendedorNaoExiste(vendedor)

            confirmacao = input(f"Tem certeza que deseja deletar o vendedor {vendedor._nome}? (S/N): ").strip()

            if confirmacao.upper() != 'S':
                raise ValueError("Operação cancelada pelo usuário.")

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
            
    def listar_vendedores_gerente(self, id_gerente):
        gerente = self._bd.query(Gerente).filter_by(id=id_gerente).first()
        if not gerente:
            print("Gerente não encontrado.")
            return

        vendedores = self._bd.query(Vendedor).filter_by(gerente_id=id_gerente).all()

        if not vendedores:
            print(f"Não existem vendedores associados a(o) gerente {gerente._nome} no momento.")
            return

        print(f"\nVendedores do(a) gerente {gerente._nome}:\n")
        for vendedor in vendedores:
            print(f"- {vendedor._nome} - ID {vendedor.id} | CPF: {vendedor._cpf}")


    def listar_vendedor(self):
        cpf = input("Digite o CPF para buscar: ").strip()
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
        try:
            cpf_limpo = Validacoes.validar_cpf(cpf)
            vendedor = self._bd.query(Vendedor).filter_by(_cpf=cpf_limpo).first()
            if not vendedor:
                raise VendedorNaoExiste(f'Vend com CPF {cpf_limpo} não encontrado.')
            print(f'Vendedor - {vendedor._nome.upper()} - ID {vendedor.id}')
            print(f'CPF - {vendedor._cpf} - E-MAIL - {vendedor._email}')
            print(f'TELEFONE - {vendedor._telefone} - DATA ENTRADA - {vendedor.data_criacao}')
            print(f'TURNO - {vendedor._turno} - SETOR - {vendedor.gerente._setor}\n')
            
            
        except (VendedorNaoExiste, CpfInvalido) as g:
            print(g)
            return
        except Exception as e:
            print(f'Erro: {e}')

    def atualizar(self, cpf):
        try: 
            cpf_limpo = Validacoes.validar_cpf(cpf)
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
                nome = input("Novo nome: ").strip()
                if len(nome) < 3:
                    raise NomeInvalido(nome)
                vendedor._nome = nome
                
            elif opcao == '2':
                email = input("Novo email: ").strip()
                email_limpo = Validacoes.validar_email(email)
                if Validacoes.email_ja_existe(self._bd, email_limpo):
                    raise EmailJaExisteException(email_limpo)
                vendedor._email = email_limpo
                
            elif opcao == '3':
                telefone = input("Novo telefone: ").strip()
                telefone_limpo = Validacoes.validar_telefone(telefone)
                if Validacoes.telefone_ja_existe(self._bd, telefone_limpo):
                    raise TelefoneJaExiste(telefone_limpo)
                vendedor._telefone = telefone_limpo
                
            elif opcao == '4':
                turno = input("Novo turno (M, T, N): ").strip().upper()
                if turno not in ['M', 'T', 'N']:
                    raise TurnoInvalido(turno)
                vendedor._turno = turno
                
            elif opcao == '5':
                print("Nenhuma alteração realizada.")
            else:
                print("Opção inválida.")

            self._bd.commit()
            print("Atualização realizada com sucesso.")
        except (VendedorNaoExiste, EmailJaExisteException, TelefoneJaExiste, TurnoInvalido, NomeInvalido, CpfInvalido) as e:
            self._bd.rollback()
            print(e)
            return
        except Exception as ex:
            self._bd.rollback()
            print('Erro de validação - ')
            return
