from abc import ABC, abstractmethod

class CRUDAbstrato(ABC):
    @abstractmethod
    def criar(self, id_gerente):
        pass

    @abstractmethod
    def listar_tudo(self):
        pass

    @abstractmethod
    def atualizar(self, cpf):
        pass

    @abstractmethod
    def deletar(self):
        pass
