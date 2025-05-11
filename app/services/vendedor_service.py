from models.vendedor import Vendedor

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
    def modificar_vendedor(cls, bd, vendedor_cpf: int):
            try:
                vendedor = bd.query(Vendedor).filter(Vendedor.cpf == vendedor_cpf).first()
                if vendedor:

                    novo_cpf_str = input(f"Alterar CPF ({vendedor.cpf} - Deixe em branco para manter: ")
                    if novo_cpf_str:
                        vendedor.cpf = int(novo_cpf_str)

                    novo_nome = input(f"Alterar nome ({vendedor.nome} - Deixe em branco para manter: ")
                    if novo_nome:
                        vendedor.nome = novo_nome

                    novo_email = input(f"Novo email ({vendedor.email} - Deixe em branco para manter: ")
                    if novo_email:
                        vendedor.email = novo_email

                    novo_telefone = input(f"Novo telefone ({vendedor.telefone} - Deixe em branco para manter: ")
                    if novo_telefone:
                        vendedor.telefone = novo_telefone

                    novo_turno = input(f"Novo turno ({vendedor.turno} - Digite M, T ou N, ou deixe em branco para manter: ").upper()
                    if novo_turno:
                        if novo_turno in ["M", "T", "N"]:
                            vendedor.turno = novo_turno
                        else:
                            print("Turno inválido. Use M, T ou N.")

                    novo_salario = input(f"Novo salário ({vendedor.salario} - Deixe em branco para manter: ")
                    if novo_salario:
                        vendedor.salario = float(novo_salario)

                    bd.commit()
                else:
                    print(f"Vendedor com CPF: {vendedor_cpf} não encontrado.")
            except:
                bd.rollback()