import re
from models.gerente import Gerente
from models.produto import Produto
from models.estoquista import Estoquista
from models.vendedor import Vendedor
from .pessoa_services import CRUDAbstrato
from utils.validacoes import Validacoes
from utils.exceptions import (
    EmailJaExisteException,
    CpfJaExistente,
    SalarioNegativo,
    TelefoneJaExiste,
    GerenteNaoExiste,
    ProdutoNaoEncontrado,
    PrecoNegativo,
    CpfInvalido,
    EstoquistaJaExiste, 
    TelefoneInvalido,
    NomeInvalido,
    TurnoInvalido
)

class GerenteService(CRUDAbstrato):
    def __init__(self, bd):
        self._bd = bd
        
    def alterar_precos(self):
        produtos = self._bd.query(Produto).all()
        if not produtos:
            return
        
        id_produto = int(input("Insira o ID do produto que deseja modificar o Preço de Venda: "))
        produto_existe = self._bd.query(Produto).filter_by(id=id_produto).first()
        if not produto_existe:
            raise ProdutoNaoEncontrado(id_produto)

        try:
            novo_preco = float(input("Qual será o novo preço de venda? "))
            if novo_preco <= 0:
                raise PrecoNegativo(novo_preco)

            produto_existe._preco_venda = novo_preco
            self._bd.commit()
            print(f"Preço do produto {produto_existe.nome} alterado para R$ {novo_preco:.2f}")
        except PrecoNegativo as e:
            self._bd.rollback()
            print(e)
        except ValueError:
            self._bd.rollback()
            print("Valor inválido. Digite um número válido para o preço.")

    def criar(self, cpf):
        try:
            nome = input("Insira o nome: ")

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

            setor = input("Qual o setor? ")
            
            gerente = Gerente(
                _nome=nome,
                _cpf=cpf_limpo,
                _email=email,
                _telefone=telefone_limpo,
                _turno=turno,
                _salario=salario,
                _setor=setor
            )

            self._bd.add(gerente)
            self._bd.commit()

            print(f"Gerente {nome} criado com sucesso.")
        except (SalarioNegativo, CpfInvalido, EmailJaExisteException, CpfJaExistente, TelefoneJaExiste, SalarioNegativo, TelefoneInvalido, TurnoInvalido) as e:
            print(e)
            self._bd.rollback()
            return
        except (Exception, ValueError) as ve:
            print("Erro de validação")
            self._bd.rollback()
            return

    def listar_tudo(self):
        gerentes = self._bd.query(Gerente).all()
        if not gerentes:
            print("Não existem gerentes cadastrados no momento.")
            return
        for gerente in gerentes:
            print(gerente)

    def listar_gerente(self):
        cpf = input("Insira o CPF (Somente números): ")
        try:
            cpf_limpo = Validacoes.validar_cpf(cpf)

            gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste(cpf_limpo)
            print(gerente)
        except (GerenteNaoExiste, CpfInvalido) as g:
            print(g)
            return
        
    def listar_dados(self, cpf):
        cpf_limpo = GerenteService.validar_cpf(cpf)

        try:
            gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste(f'Gerente com CPF {cpf_limpo} não encontrado.')
            print(gerente)
        except GerenteNaoExiste as g:
            print(g)
            return
        
    def atualizar(self, cpf):
        cpf_limpo = Validacoes.validar_cpf(cpf)
        gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
        
        try:
            if not gerente:
                raise GerenteNaoExiste(f'Gerente com CPF {cpf_limpo} não encontrado.')

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
                gerente._nome = nome

            elif opcao == '2':
                email = input("Novo email: ")
                if Validacoes.email_ja_existe(self._bd, email):
                    raise EmailJaExisteException(email)
                gerente._email = email

            elif opcao == '3':
                telefone = input("Novo telefone: ")
                telefone_limpo = Validacoes.validar_telefone(telefone)
                if Validacoes.telefone_ja_existe(self._bd, telefone_limpo):
                    raise TelefoneJaExiste(telefone_limpo)
                gerente._telefone = telefone_limpo

            elif opcao == '4':
                turno = input("Novo turno (M, T ou N): ").upper()
                if turno not in ['M', 'T', 'N']:
                    raise TurnoInvalido(turno)
                gerente._turno = turno

            elif opcao == '5':
                print("Nenhuma alteração realizada.")
                return

            else:
                print('Opção inválida. Tente novamente.')
                return

            self._bd.commit()
            print("Gerente atualizado com sucesso.")
        except (GerenteNaoExiste, EmailJaExisteException, TelefoneJaExiste, NomeInvalido,TurnoInvalido) as e:
            print(e)
            self._bd.rollback()
            return
            
        except Exception as e:
            print('Erro de validação - ')
            self._bd.rollback()
            return

    def deletar(self):
        try:
            cpf = input("Insira o CPF do Gerente que deseja deletar (SOMENTE NÚMEROS): ")
            cpf_limpo = Validacoes.validar_cpf(cpf)

            gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste("O gerente não existe.")
            
            confirmacao = input(f"Tem certeza que deseja deletar o gerente: {gerente._nome}? (S/N): ")

            if confirmacao.upper() != 'S':
                print("Operação cancelada pelo usuário.")
                return

            self._bd.delete(gerente)
            self._bd.commit()
            print("Gerente removido com sucesso!")
        except (GerenteNaoExiste, CpfInvalido) as e:
            self._bd.rollback()
            print(e)
            return
            
