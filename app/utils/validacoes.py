from models.estoquista import Estoquista
from models.gerente import Gerente
from models.vendedor import Vendedor
from .exceptions import (TelefoneInvalido, CpfInvalido, EmailInvalido)
import re

class Validacoes:
    
    @staticmethod
    def cpf_ja_existe(bd, cpf):
        return any([
            bd.query(Gerente).filter_by(_cpf=cpf).first(),
            bd.query(Vendedor).filter_by(_cpf=cpf).first(),
            bd.query(Estoquista).filter_by(_cpf=cpf).first(),
        ])
    
    @staticmethod
    def telefone_ja_existe(bd, telefone):
        return any([
            bd.query(Gerente).filter_by(_telefone=telefone).first(),
            bd.query(Vendedor).filter_by(_telefone=telefone).first(),
            bd.query(Estoquista).filter_by(_telefone=telefone).first(),
        ])

    @staticmethod
    def email_ja_existe(bd, email):
        return any([
            bd.query(Gerente).filter_by(_email=email).first(),
            bd.query(Vendedor).filter_by(_email=email).first(),
            bd.query(Estoquista).filter_by(_email=email).first(),
        ])
    
    @staticmethod
    def salario_negativo(salario):
        if salario < 0:
            return True
        
    @staticmethod
    def validar_cpf(cpf):
        cpf_limpo = re.sub(r'\D', '', cpf)
        if len(cpf_limpo) != 11:
            raise CpfInvalido(cpf_limpo)
        return cpf_limpo
    
    @staticmethod
    def validar_telefone(telefone):
        telefone_limpo = re.sub(r'\D', '', telefone)
        if len(telefone_limpo) > 14:
            raise TelefoneInvalido(telefone_limpo)
        return telefone_limpo
    
    @staticmethod
    def validar_email(email):
        if len(email) < 15:
            raise EmailInvalido(email)
        return email