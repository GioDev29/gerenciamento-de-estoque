from models.estoquista import Estoquista
from utils.exceptions import DuplicidadeDeCpf, DuplicidadeDeTelefone
from sqlalchemy import exc

class EstoquistaService:
    
    def criar_estoquista(bd):
        try:
            nome = input("Insira o nome: ")
            cpf = int(input("Insira o cpf (SOMENTE NÚMEROS): "))
            email = input("Insira o E-mail: ")
            telefone = input("Insira o Telefone: ")
            turno = input("Insira o o Turno(M, T, N): ").upper()
            salario = float(input("Insira o Salário: "))

            if salario <= 0:
                raise ValueError("Salário deve ser maior que zero!")
            if turno not in ['M', 'T', 'N']:
                raise ValueError("Turno inválido! Use M, T ou N.")
            
            estoquista = Estoquista(nome=nome,cpf=str(cpf),email=email,telefone=telefone,turno=turno,salario=salario)
            bd.add(estoquista)
            bd.commit()
            print("Estoquista cadastrado com sucesso!")
            
        except ValueError as ve:
            bd.rollback()
            print(f"Erro de validação: {ve}")
        except sqlalchemy.exc.IntegrityError as ie:
            bd.rollback()
            if "cpf" in str(ie).lower():
                print("Erro: CPF já cadastrado!")
            elif "telefone" in str(ie).lower():
                print("Erro: Telefone já cadastrado!")
            elif "email" in str(ie).lower():
                print("Erro: E-mail já cadastrado!")
            else:
                print(f"Erro de integridade no banco de dados: {ie}")
        except Exception as e:
            bd.rollback()
            print(f"Erro inesperado: {e}")
            
    def listar_estoquistas(bd):
        estoquistas = bd.query(Estoquista).all
        for estoquista in estoquistas:
            print(estoquista)
            
    def listar_estoquista(bd):
        cpf = int(input())
        estoquista = bd.query(Estoquista).filter_by(cpf=cpf).first()
        if not estoquista:
            print(f'O vendedor do "{cpf}" não foi  encontrado.')
            return
        else:
            print(estoquista)

    def deletar_estoquista(bd):
        try:
            cpf = int(input("Insira o cpf(Somente números): "))
            estoquista = bd.query(Estoquista).filter_by(cpf=cpf).first()

            if not estoquista:
                print("O estoquista não exite.")
                return
            
            confirmacao = input(f"Tem certeza que deseja deletar o estoquista {estoquista.nome}? (S/N): ")

            if confirmacao.upper() != 'S':
                print("Operação cancelada pelo usuário.")
                return
            
            bd.delete(estoquista)
            bd.commit()

            print("Estoquista removido com sucesso!")
            return
    
        except Exception as e:
            bd.rollback()
