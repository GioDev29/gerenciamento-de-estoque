from models import Vendedor

class VendedorService:
    
    
    def criar_vendedor(bd):
        try:
            nome = input("Insira o nome: ")
            cpf = int(input("Insira o cpf (SOMENTE NÚMEROS): "))
            email = input("Insira o E-mail: ")
            telefone = input("Insira o Telefone: ")
            turno = input("Insira o o Turno(M, T, N): ")
            salario = float(input("Insira o Salário: "))
            
            vendedor = Vendedor(nome=nome,cpf=str(cpf),email=email,telefone=telefone,turno=turno,salario=salario)
            bd.add(vendedor)
            bd.commit()
        except :
            #Erro de duplicidade de cpf
            #Erro de duplicidade de telefone
            #Erro de salario negativo ou menor que 0
            #Erro se não for um turno válido
            bd.rollback()
            pass
    
    def deletar_vendedor(bd):
        cpf = int(input())
        try:
            vendedor = bd.query(Vendedor).filter(cpf=cpf).first()
            if vendedor:
                bd.delete(vendedor)
                bd.commit()
        except:
            bd.rollback()
    
    def listar_vendedores(bd):
        vendedores = bd.query(Vendedor).all
        for vendedor in vendedores:
            print(vendedor)
            
    def listar_vendedor(bd):
        cpf = int(input())
        vendedor = bd.query(Vendedor).filter_by(cpf=cpf).first()
        if not vendedor:
            print(f'O vendedor do "{cpf}" não foi  encontrado.')
            return
        else:
            print(vendedor)
        
    
    