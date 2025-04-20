from app.main import bd
from models import Vendedor

class VendedorService:
    
    # Vamos usar esse class metodo pq se n vai ter que criar instancia e é chato :PP
    # Quanfo a gente usa o Session ali embaixo a gente está persisti
    @classmethod
    def criar_vendedor(cls, session: bd):
        try:
            nome = input("Insira o nome: ")
            cpf = int(input("Insira o cpf (SOMENTE NÚMEROS): "))
            email = input("Insira o E-mail: ")
            telefone = input("Insira o Telefone: ")
            turno = input("Insira o o Turno(M, T, N): ")
            salario = float(input("Insira o Salário: "))
            
            vendedor = Vendedor(nome=nome,cpf=str(cpf),email=email,telefone=telefone,turno=turno,salario=salario)
            session.add(vendedor)
            session.commit()
        except :
            #Erro de duplicidade de cpf
            #Erro de duplicidade de telefone
            #Erro de salario negativo ou menor que 0
            #Erro se não for um turno válido
            session.rollback()
            pass
    
    def listar_vendedores(cls):
        vendedores = bd.query(Vendedor).all
        for vendedor in vendedores:
            print(vendedor)
            
    def listar_vendedor(cls, cpf):
        cpf = int(input())
        vendedor = bd.query(Vendedor).filter_by(cpf=cpf).first()
        if not vendedor:
            print(f'O vendedor do "{cpf}" não foi  encontrado.')
            return
        else:
            print(vendedor)
        
    
    