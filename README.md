# Sistema de Gerenciamento de Estoque

Sistema de controle de estoque focado em diferentes perfis de usuários: **Gerente**, **Vendedor** e **Estoquista**.

> Desenvolvido com **Programação Orientada a Objetos** e utilizando o **SQLAlchemy** como ORM para a comunicação com o banco de dados.

---

## Visão Geral do Projeto

O sistema permite o gerenciamento completo do estoque, produtos e movimentações internas, além de cadastro e administração dos usuários envolvidos na operação.

### Perfis de Acesso
- **Gerente**
- **Vendedor**
- **Estoquista**

---

## Tecnologias Utilizadas
- **Python 3.11+**
- **SQLAlchemy ORM**
- **POO (Programação Orientada a Objetos)**

---

## Estrutura do Projeto
```
app/
├── database/   # Conexão e configuração do banco de dados
├── models/     # Modelos das tabelas (ORM)
├── services/   # Lógica 
└── utils/      # Funções utilitárias
```

---

## Tabelas do Banco de Dados
- **Vendedor**
- **Gerente**
- **Estoquista**
- **Estoque**
- **Produto**
- **Movimentação de Estoque**

---

## Funcionalidades
- **CRUD** de Vendedor e Estoquista
- **CRUD** de Estoque e Produtos
- **CRUD** de Movimentações de Estoque
- Visualizar movimentações específicas
- Atualização dinâmica de estoque (entrada e saída de produtos)

---

## Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.
