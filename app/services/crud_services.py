from abc import ABC, abstractmethod

class CRUDAbstrato(ABC):
    @abstractmethod
    def criar(self, cod_identificacao):
        pass

    @abstractmethod
    def listar_tudo(self):
        pass

    @abstractmethod
    def atualizar(self, cod_identificacao):
        pass

    @abstractmethod
    def deletar(self):
        pass
    
    
