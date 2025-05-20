import re
from models.gerente import Gerente
from models.produto import Produto
from utils.exceptions import (
    EmailJaExisteException,
    CpfJaExistente,
    SalarioNegativo,
    TelefoneJaExiste,
    GerenteNaoExiste,
    ProdutoNaoEncontrado,
    PrecoNegativo
)

class GerenteService:
    def __init__(self, bd):
        self._bd = bd
        
    @staticmethod
    def validar_cpf(cpf):
        cpf_limpo = re.sub(r'\D', '', cpf)
        if len(cpf_limpo) != 11:
            raise ValueError("CPF inválido: deve conter 11 números.")
        
        return cpf_limpo
    
    '''
    Modificar em todas as classes
    '''
    
        
    def alterar_precos(self, id_produto):
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

    def criar_gerente(self):
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

        
        if self._bd.query(Gerente).filter_by(email=email).first():
            raise EmailJaExisteException(email)

        if self._bd.query(Gerente).filter_by(cpf=cpf_limpo).first():
            raise CpfJaExistente(cpf_limpo)

        if self._bd.query(Gerente).filter_by(telefone=telefone_limpo).first():
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

        self._bd.add(gerente)
        self._bd.commit()

        print(f"Gerente {nome} criado com sucesso.")

    def listar_gerentes(self):
        gerentes = self._bd.query(Gerente).all()
        for gerente in gerentes:
            print(gerente)

    def listar_gerente(self):
        cpf = input("Insira o CPF (Somente números): ")
        cpf_limpo = re.sub(r'\D', '', cpf)

        gerente = self._bd.query(Gerente).filter_by(cpf=cpf_limpo).first()
        if not gerente:
            raise GerenteNaoExiste(f'Gerente com CPF {cpf_limpo} não encontrado.')
        print(gerente)

    def atualizar_gerente(self, cpf):
        cpf_limpo = re.sub(r'\D', '', cpf)
        gerente = self._bd.query(Gerente).filter_by(cpf=cpf_limpo).first()

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
            gerente.nome = nome

        elif opcao == '2':
            email = input("Novo email: ")
            if self._bd.query(Gerente).filter_by(email=email).first():
                raise EmailJaExisteException(email)
            gerente.email = email

        elif opcao == '3':
            telefone = input("Novo telefone: ")
            telefone_limpo = re.sub(r'\D', '', telefone)
            if self._bd.query(Gerente).filter_by(telefone=telefone_limpo).first():
                raise TelefoneJaExiste(telefone_limpo)
            gerente.telefone = telefone_limpo

        elif opcao == '4':
            turno = input("Novo turno (M, T ou N): ").upper()
            if turno not in ['M', 'T', 'N']:
                raise Exception("Turno inválido! Use apenas: M (Manhã), T (Tarde) ou N (Noite).")
            gerente.turno = turno

        elif opcao == '5':
            print("Nenhuma alteração realizada.")
            return

        else:
            print('Opção inválida. Tente novamente.')
            return

        self._bd.commit()
        print("Gerente atualizado com sucesso.")

    def deletar_gerente(self):
        try:
            cpf = input("Insira o CPF (SOMENTE NÚMEROS): ")
            cpf_limpo = re.sub(r'\D', '', cpf)

            gerente = self._bd.query(Gerente).filter_by(cpf=cpf_limpo).first()
            if not gerente:
                raise GerenteNaoExiste("O gerente não existe.")

            self._bd.delete(gerente)
            self._bd.commit()
            print("Gerente deletado com sucesso.")
        except GerenteNaoExiste as e:
            self._bd.rollback()
            print(str(e))
