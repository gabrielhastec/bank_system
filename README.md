# 🔐 Bank System

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![Tests](https://img.shields.io/badge/Tests-pytest-green)
![Coverage](https://img.shields.io/badge/Coverage-Em%20breve-lightgrey)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Autor:** Gabriel Rodrigues  
> **Versão:** 1.0 (em desenvolvimento)  
> **Contato:** gabrielhastec.dev@gmail.com > **Data de Início:** 21/08/2025

---

## 📖 Descrição

O **Bank System** é um **mini framework bancário em Python**, desenvolvido para gerenciar **contas, transações, depósitos, saques e extratos** de forma **modular, testável e segura**.

O projeto segue **boas práticas de desenvolvimento**:

- Docstrings completas e padronizadas de acordo com **PEP 257**
- Estrutura modular, facilitando integração com outros sistemas
- Testes unitários implementados com **pytest**
- Exceções personalizadas para erros financeiros
- Código em constante evolução, preparado para novas funcionalidades

> ⚠️ Este projeto ainda está em construção e receberá melhorias contínuas.

---

## 🗂 Estrutura do Projeto

```

bank\_system/
│
├── bank/
│   ├── **init**.py
│   ├── exceptions.py       # Exceções personalizadas
│   ├── core/
│   │   ├── **init**.py
│   │   ├── db.py           # Configuração do banco de dados SQLite
│   │   └── schema.py       # Definição do esquema do banco de dados
│   ├── data/
│   │   └── bank.db
│   ├── models/
│   │   ├── **init**.py
│   │   ├── account.py      # Classe Account para gerenciamento de contas
│   │   └── transaction.py  # Classe Transaction para registro de transações
│   ├── repositories/
│   │   ├── **init**.py
│   │   └── account_repo.py # Repositório para operações no banco de dados
│   ├── services/
│   │   ├── **init**.py
│   │   └── account_service.py # Regras de negócio para contas e transações
│   └── utils/
│       ├── **init**.py
│       └── validators.py   # Funções de validação
│
├── cli/
│   ├── **init**.py
│   └── menu.py             # Interface CLI para interação com o usuário
│
├── data/
│   └── .gitkeep
│
├── examples/
│   └── main.py             # Script de exemplo para executar o sistema
│
├── migrations/
│   └── increments.py       # Script para gerenciamento de migrações
│
├── test/
│   ├── **init**.py
│   ├── conftest.py         # Configuração de fixtures para testes
│   ├── test_account.py     # Testes unitários do AccountService
│   └── test_repository.py  # Testes unitários do AccountRepository
│
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
└── setup.py

```

---

## ⚡ Funcionalidades Atuais

- Gestão de contas:
  - Criação de contas com CPF, nome e saldo inicial.
  - Persistência de contas em banco de dados SQLite.
- Depósitos e saques com validações:
  - Validações de valores positivos e saldo suficiente.
  - Registro de transações no banco de dados.
- Transferências entre contas:
  - Transferências seguras com validação de saldo.
  - Registro de transações de origem e destino.
- Extrato de transações:
  - Recuperação de histórico de transações por conta.
  - Ordenação por data/hora.
- Interface CLI:
  - Menu interativo para operações bancárias via terminal.
- Exceções personalizadas:
  - ValorInvalidoError para valores zero ou negativos.
  - SaldoInsuficienteError para saques/transferências sem saldo.
  - ContaNaoEncontradaError para contas inexistentes.
  - ContaDuplicadaError para CPFs duplicados.

---

## 🧪 Testes

- Cobertura de operações válidas e inválidas
- Testes de exceções personalizadas
- Implementado com **pytest**
- **Executando os testes:**

```bash
pytest -v
```

> Cobertura completa será adicionada em versões futuras.

---

## 🛠 Tecnologias Utilizadas

- **Python 3.13**
- **SQLite** (persistência de dados).
- **pytest** (testes unitários).
- **Git / GitHub** (controle de versão).
- Estrutura modular orientada a objetos
- Docstrings seguindo **PEP 257**

---

## 🚀 Roadmap / Próximas Implementações

O projeto está planejado para evoluir com:

1. **Melhorias no extrato:**

   - Filtragem por tipo de transação ou período
   - Formatação em tabela e exportação CSV/JSON

2. **Interface CLI aprimorada:**

   - Suporte a comandos mais intuitivos.
   - Feedback visual mais claro para o usuário.

3. **Interface CLI ou GUI**

   - Desenvolvimento de uma interface com Tkinter ou similar.

4. **API REST:**

   - Integração com sistemas externos via endpoints REST.

5. **Documentação e Licença**

   - Licença MIT a ser adicionada
   - Documentação detalhada das classes e métodos

---

## Versões futuras

- v1.1: Exportação de extratos e melhorias na CLI.
- v1.2: Suporte inicial a API REST.
- v2.0: Interface gráfica e cobertura completa de testes.

---

## 📌 Contatos e Suporte

- **Autor:** Gabriel Rodrigues
- **E-mail:** [gabrielhastec.dev@gmail.com](mailto:gabrielhastec.dev@gmail.com)
- **LinkedIn:** [linkedin.com/in/gabrielhastec](https://www.linkedin.com/in/gabrielhastec)

> Fique à vontade para abrir issues, sugerir melhorias ou contribuir com pull requests.

---

## ⚖ Licença

Este projeto é atualmente destinado a fins educacionais e demonstração de aprendizado pessoal.  
Embora não possua uma licença formal aplicada no momento, estou familiarizado com licenças de código aberto reconhecidas, como MIT, GPL e Apache.

Planejo aplicar a licença MIT futuramente caso o projeto evolua para distribuição pública.  
Enquanto isso, o código pode ser estudado, adaptado e referenciado para fins de aprendizado, mas não deve ser usado em produção sem autorização.
