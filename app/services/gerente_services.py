from models import Gerente

class GerenteServices:
    
    @staticmethod
    def criar_gerente(bd):
        try:
            nome = input("Insira o nome: ")
            cpf = int(input("Insira o cpf (SOMENTE NÚMEROS): "))
            email = input("Insira o E-mail: ")
            telefone = input("Insira o Telefone: ")
            turno = input("Insira o o Turno(M, T, N): ")
            salario = float(input("Insira o Salário: "))
            setor = input("Qual o setor? ")
            
            gerente = Gerente(nome=nome,cpf=str(cpf),email=email,telefone=telefone,turno=turno,salario=salario, setor=setor)
            bd.add(gerente)
            bd.commit()
        except Exception as e:
            #Erro de duplicidade de cpf
            #Erro de duplicidade de telefone
            #Erro de salario negativo ou menor que 0
            #Erro se não for um turno válido
            bd.rollback()
            pass
    
    def listar_gerentes(bd):
        gerentes = bd.query(Gerente).all
        for gerente in gerentes:
            print(gerente)
            
    def listar_gerente(bd):
        cpf = int(input("Insira o cpf(Somente números): "))
        gerente = bd.query(Gerente).filter_by(cpf=cpf).first()
        if not gerente:
            print(f'O vendedor do "{cpf}" não foi  encontrado.')
            return
        else:
            print(gerente)
            
    def deletar_gerente(bd):
        try:
            cpf = int(input("Insira o cpf(Somente números): "))
            gerente = bd.query(Gerente).filter_by(cpf=cpf).first()
            if not gerente:
                print("O gerente não exite.")
                return
            
            bd.delete()
            bd.commit()
        except Exception as e:
            bd.rollback()
            
        
        
        

        
    