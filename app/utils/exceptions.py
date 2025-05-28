class DuplicidadeDeCpf(Exception):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"O CPF '{self.cpf}' já está cadastrado.")

class DuplicidadeDeTelefone(Exception):
    def __init__(self, telefone):
        self.telefone = telefone
        super().__init__(f"O telefone '{self.telefone}' já está cadastrado.")
        
class TelefoneJaExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O telefone {self.tipo} já existe. Tente novamente")

class TelefoneInvalido(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O telefone {self.tipo} é inválido. Ex: +55 11 999999999")

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

class SemMovimentacaoError(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(f"Tipo de movimentação inválido: '{self.tipo}'.")

class TipoUsuarioError(Exception):
    def __init__(self, tipo_usuario):
        self.tipo_usuario = tipo_usuario
        super().__init__(f"Tipo de usuário inválido: '{self.tipo_usuario}'.")

class ErroNaQuantidade(Exception):
    def __init__(self, qtd):
        self.qtd = qtd
        super().__init__(f"A quantidade '{self.qtd}' é inválida. Deve ser maior que zero.")

class SalarioNegativo(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O salário não pode ser negativo.")
        
class PrecoNegativo(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O preço não pode ser negativo ou igual a zero.")



class EstoquistaJaExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O Estoquista {self.tipo} já existe. Tente novamente")


class GerenteNaoExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O gerente: {self.tipo} não existe.")
        
class VendedorNaoExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O vendedor: {self.tipo} não existe.")

class EstoquistaNaoExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O estoquista: {self.tipo} não existe.")

class CpfJaExistente(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O CPF: {self.tipo} já existe.")

class CpfInvalido(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O CPF: {self.tipo} precisa ter 11 digitos.")

class ProdutoNaoExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O Produto: {self.tipo} não existe.")
        
class ProdutoJaExiste(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O Produto: {self.tipo} já existe.")

class IdVazio(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O ID não pode ser vazio.")

class NomeInvalido(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O Nome: {self.tipo} é inválido, precisa ter mais que 2 letras.")

class TurnoInvalido(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O Turno: {self.tipo} é inválido. Somente M(Manhã), T(Tarde) e N(Noite).")

class EmailInvalido(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O E-mail: {self.tipo} é inválido, precisa ter mais que 14 letras.")

class ValorInvalido(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O valor: {self.tipo} é inválido, não pode ser negativo ou igual a zero.")
        
class TextoInvalido(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        super().__init__(F"O Texto: {self.tipo} é inválido, não pode ter menos que 3 caracteres.")