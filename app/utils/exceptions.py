class DuplicidadeDeCpf(Exception):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"O CPF '{self.cpf}' já está cadastrado.")

class DuplicidadeDeTelefone(Exception):
    def __init__(self, telefone):
        self.telefone = telefone
        super().__init__(f"O telefone '{self.telefone}' já está cadastrado.")

class EmailJaExisteException(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"O e-mail '{self.email}' já está cadastrado.")

class ProdutoNaoEncontrado(Exception):
    def __init__(self, codigo_produto):
        self.codigo = codigo_produto
        super().__init__(f"Produto com código '{self.codigo}' não foi encontrado.")

class UsuarioNaoEncontrado(Exception):
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        super().__init__(f"Usuário com ID '{self.id_usuario}' não foi encontrado.")

class GerenteNaoExiste(Exception):
    def __init__(self, id_gerente):
        self.id_gerente = id_gerente
        super().__init__(f"O gerente com ID '{self.id_gerente}' não existe.")

class SemMovimentacaoError(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(f"Tipo de movimentação inválido: '{self.tipo}'.")

class TipoUsuaioError(Exception):
    def __init__(self, tipo_usuario):
        self.tipo_usuario = tipo_usuario
        super().__init__(f"Tipo de usuário inválido: '{self.tipo_usuario}'.")

class ErroNaQuantidade(Exception):
    def __init__(self, qtd):
        self.qtd = qtd
        super().__init__(f"A quantidade '{self.qtd}' é inválida. Deve ser maior que zero.")

class SalarioNegativo(Exception):
    def __init__(self, valor):
        self.valor = valor
        super().__init__(f"Salário inválido: {self.valor}. Deve ser maior que zero.")
