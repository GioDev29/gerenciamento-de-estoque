from models.movimentarEstoque import MovimentacaoEstoque

class MovimentarEstoque:
    
    def criar_mov_estoque(bd):
        try:
            tipo = input("Insira o tipo(Entrada/Saida): ").lower()
            produto_id = int(input("Insira o ID do produto: "))
            tipo_user = input("Gerente, Estoquista ou Vendedor? ")
            id_user = input("Insira o seu ID ")
            quantidade = input("Insira a quantidade que será movimentada ")
            
            mov_estoque = MovimentacaoEstoque(tipo=tipo,produto_id=produto_id, tipo_user=tipo_user, id_user=id_user, quantidade=quantidade)
            bd.add(mov_estoque)
            bd.commit()
        except Exception as e:
            #Erro de duplicidade de cpf
            #Erro de duplicidade de telefone
            #Erro de salario negativo ou menor que 0
            #Erro se não for um turno válido
            bd.rollback()
            pass
    
    def listar_movs_estoque(bd):
        mov_estoque = bd.query(MovimentacaoEstoque).all
        for mov in mov_estoque:
            print(mov)
            
    def listar_mov_estoque(bd):
        tipo = input("Insira se você quer ver as Entradas ou Saidas(Entrada/Saida): ").lower()
        mov_estoque = bd.query(MovimentacaoEstoque).filter_by(tipo=tipo).all
        if not mov_estoque:
            print(f'A movimentação do tipo {tipo}, não foi encontrada.')
            return
        else:
            print(mov_estoque)
            
    def listar_mov_estoque_produto(bd):
        produto_id = input("Insira o ID do produto que deseja ver: ").lower()
        mov_estoque = bd.query(MovimentacaoEstoque).filter_by(produto_id=produto_id).all
        if not mov_estoque:
            print(f'Não tem movimentação do produto com o ID {produto_id}')
            return
        else:
            print(mov_estoque)
            

            
        
        
        

        
    