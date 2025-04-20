# O __init__.py serve para importar de forma mais fácil os arquivos
# Torna a pasta um pacote Python
# Permite importações mais limpas

from .produto import Produto
from .vendedor import Vendedor
from .estoque import Estoque
from .movimentarEstoque import movimentarEstoque
from .gerente import Gerente
from .pessoa import Pessoa