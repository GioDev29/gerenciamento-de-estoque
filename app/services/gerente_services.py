from models import Produto, Gerente, Estoque, MovimentacaoEstoque, Estoquista, Vendedor
from .crud_services import CRUDAbstrato
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
    TurnoInvalido,
    EmailInvalido
)

class GerenteService(CRUDAbstrato):
    def __init__(self, bd):
        self._bd = bd
        
    def alterar_precos(self):
        produtos = self._bd.query(Produto).all()
        if not produtos:
            print('Não existem produtos adicionados.')
            return
        
        id_produto = int(input("Insira o ID do produto que deseja modificar o Preço de Venda: ").strip())
        produto_existe = self._bd.query(Produto).filter_by(id=id_produto).first()
        if not produto_existe:
            raise ProdutoNaoEncontrado(id_produto)

        try:
            novo_preco = float(input("Qual será o novo preço de venda? ").replace(",", "."))
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
            nome = input("Insira o nome: ").strip()
            if len(nome) < 3:
                raise NomeInvalido(nome)
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

            turno = input("Insira o Turno (M, T, N): ").strip().upper()
            if turno not in ['M', 'T', 'N']:
                raise TurnoInvalido(turno)

            salario = float(input("Insira o Salário: ").strip().replace(",", "."))
            if Validacoes.salario_negativo(salario):
                raise SalarioNegativo(salario)

            setor = input("Qual o setor? ").strip()
            
            gerente = Gerente(
                _nome=nome,
                _cpf=cpf_limpo,
                _email=email_limpo,
                _telefone=telefone_limpo,
                _turno=turno,
                _salario=salario,
                _setor=setor
            )

            self._bd.add(gerente)
            self._bd.commit()

            print(f"Gerente {nome} criado com sucesso.")
        except (SalarioNegativo, CpfInvalido, EmailJaExisteException, CpfJaExistente, TelefoneJaExiste, SalarioNegativo, TelefoneInvalido, TurnoInvalido, EmailInvalido, NomeInvalido) as e:
            print(e)
            self._bd.rollback()
            return
        except Exception as e:
            print(f"Erro de validação: {e}")
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
        cpf = input("Insira o CPF (Somente números): ").strip()
        try:
            cpf_limpo = Validacoes.validar_cpf(cpf)

            gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste(cpf_limpo)
            print(gerente)
        except (GerenteNaoExiste, CpfInvalido) as g:
            print(g)
            return
        except Exception as e:
            print(f'Erro: {e}')
            return
        
    def listar_funcionarios(self, id_gerente):
        estoquistas = self._bd.query(Estoquista).filter_by(gerente_id=id_gerente).all()
        vendedores = self._bd.query(Vendedor).filter_by(gerente_id=id_gerente).all()
        gerente = self._bd.query(Gerente).filter_by(id=id_gerente).first()
        try: 
            if not estoquistas and not vendedores:
                raise ValueError(f"Não existem estoquistas e vendedores associados a(o) gerente {gerente._nome} no momento.")

            if estoquistas:
                print(f"\nEstoquistas do gerente {gerente._nome}:\n")
                for estoquista in estoquistas:
                    print(f"- {estoquista.id} - {estoquista._nome} | E-mail: {estoquista._email} | Telefone:  {estoquista._telefone}")

            if vendedores:
                print(f"\nVendedores do gerente {gerente._nome}:\n")
                for vendedor in vendedores:
                    print(f"- {vendedor.id} - {vendedor._nome} | E-mail: {vendedor._email} | Telefone:  {vendedor._telefone}")
        except Exception as e:
            print(f'Erro: {e}')
            return
        
    def listar_dados(self, cpf):
        try:
            cpf_limpo = Validacoes.validar_cpf(cpf)
            gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste(f'Gerente com CPF {cpf_limpo} não encontrado.')
            print(f'GERENTE - {gerente._nome.upper()} - ID {gerente.id}')
            print(f'CPF - {gerente._cpf} - E-MAIL - {gerente._email}')
            print(f'TELEFONE - {gerente._telefone} - DATA ENTRADA - {gerente.data_criacao}')
            print(f'TURNO - {gerente._turno} - SETOR - {gerente._setor}\n')
            
            
        except (GerenteNaoExiste, CpfInvalido) as g:
            print(g)
            return
        except Exception as e:
            print(f'Erro: {e}')
        
    def atualizar(self, cpf):
        try:
            cpf_limpo = Validacoes.validar_cpf(cpf)
            gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
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
                nome = input("Novo nome: ").strip()
                if len(nome) < 3:
                    raise NomeInvalido(nome)
                gerente._nome = nome

            elif opcao == '2':
                email = input("Novo email: ").strip()
                email_limpo = Validacoes.validar_email(email)
                if Validacoes.email_ja_existe(self._bd, email_limpo):
                    raise EmailJaExisteException(email_limpo)
                gerente._email = email_limpo

            elif opcao == '3':
                telefone = input("Novo telefone: ").strip()
                telefone_limpo = Validacoes.validar_telefone(telefone)
                if Validacoes.telefone_ja_existe(self._bd, telefone_limpo):
                    raise TelefoneJaExiste(telefone_limpo)
                gerente._telefone = telefone_limpo

            elif opcao == '4':
                turno = input("Novo turno (M, T ou N): ").strip().upper()
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
        except (GerenteNaoExiste, EmailJaExisteException, TelefoneJaExiste, NomeInvalido,TurnoInvalido, EmailInvalido) as e:
            print(e)
            self._bd.rollback()
            return
            
        except Exception as e:
            print(f'Erro de validação - {e}')
            self._bd.rollback()
            return

    def deletar(self):
        try:
            cpf = input("Insira o CPF do Gerente que deseja deletar (SOMENTE NÚMEROS): ").strip()
            cpf_limpo = Validacoes.validar_cpf(cpf)

            gerente = self._bd.query(Gerente).filter_by(_cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste("O gerente não existe.")
            
            confirmacao = input(f"Tem certeza que deseja deletar o gerente: {gerente._nome}? (S/N): ").strip()

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
        except Exception as e:
            print(f'Erro: {e}')
            self._bd.rollback()
            return
            
