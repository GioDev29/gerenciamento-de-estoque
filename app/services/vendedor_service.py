from models import Vendedor

class VendedorService:
    
    @staticmethod
    def criar_vendedor(session):
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
    @classmethod
    def deletar_vendedor(cls, session: bd, vendedor_cpf: int):
        try:
            vendedor = bd.query(Vendedor).filter(Vendedor.cpf == vendedor_cpf).first()
            if vendedor:
                session.delete(vendedor)
                session.commit()
        except:
            session.rollback()
    
    def listar_vendedores(bd):
        vendedores = bd.query(Vendedor).all
        for vendedor in vendedores:
            print(vendedor)
            
<<<<<<< HEAD
    def listar_ve(bd):
=======
    def listar_vendedor(cls, cpf):
>>>>>>> 0ce58418c25e6efa6d49313ecda4f5ff98197760
        cpf = int(input())
        vendedor = bd.query(Vendedor).filter_by(cpf=cpf).first()
        if not vendedor:
            print(f'O vendedor do "{cpf}" não foi  encontrado.')
            return
        else:
            print(vendedor)
        
    
    