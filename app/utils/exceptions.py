class DuplicidadeDeCpf(Exception):
    pass

class DuplicidadeDeTelefone(Exception):
    pass

class ProdutoNaoEncontrado(Exception):
    def __init__(self, codigo_produto):
        self.codigo = codigo_produto
        super().__init__(F"Produto com código {self.codigo} não foi encontrado no estoque.")
        
class SemMovimentacaoError(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"Não existe esse tipo de movimentação {self.tipo} no estoque.")

class EmailJaExisteException(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O e-mail {self.tipo} já existe. Tente novamente")
        
class CpfJaExistente(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O CPF {self.tipo} já existe. Tente novamente")
        
class SalarioNegativo(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O salário não pode ser negativo.")

class TelefoneJaExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O telefone {self.tipo} já existe. Tente novamente")

class GerenteNaoExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O gerente: {self.tipo} não existe.")

class VendedorNaoExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O vendedor: {self.tipo} não existe.")

class ProdutoNaoExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O vendedor: {self.tipo} não existe.")