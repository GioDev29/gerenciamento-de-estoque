from models.estoquista import Estoquista

class EstoquistaService:
    
    @classmethod
    def criar_estoquista(cls, session: bd):
        try:
            nome = input("Insira o nome: ")
            cpf = int(input("Insira o cpf (SOMENTE NÚMEROS): "))
            email = input("Insira o E-mail: ")
            telefone = input("Insira o Telefone: ")
            turno = input("Insira o o Turno(M, T, N): ")
            salario = float(input("Insira o Salário: "))
            
            estoquista = Estoquista(nome=nome,cpf=str(cpf),email=email,telefone=telefone,turno=turno,salario=salario)
            session.add(estoquista)
            session.commit()
        except :
            #Erro de duplicidade de cpf
            #Erro de duplicidade de telefone
            #Erro de salario negativo ou menor que 0
            #Erro se não for um turno válido
            session.rollback()
            pass
    
    def listar_estoquistas(cls):
        estoquistas = bd.query(Estoquista).all
        for estoquista in estoquistas:
            print(estoquista)
            
    def listar_estoquista(cls):
        cpf = int(input())
        estoquista = bd.query(Estoquista).filter_by(cpf=cpf).first()
        if not estoquista:
            print(f'O vendedor do "{cpf}" não foi  encontrado.')
            return
        else:
            print(estoquista)
            
        
    
    