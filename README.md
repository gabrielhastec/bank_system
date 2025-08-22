
```markdown
# 🔐 Bank System

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![Tests](https://img.shields.io/badge/Tests-pytest-green)
![Coverage](https://img.shields.io/badge/Coverage-Em%20breve-lightgrey)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Autor:** Gabriel Rodrigues  
> **Versão:** 1.0 (em desenvolvimento)  
> **Contato:** gabrielhastec.dev@gmail.com 
> **Data de Início:** 21/08/2025  

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
│   ├── account.py          # Classe Account com depósitos, saques, extrato e validações
│   ├── transaction.py      # Classe Transaction para registrar operações
│   └── exceptions.py       # Exceptions personalizadas
│
├── tests/
│   ├── **init**.py
│   ├── test\_account.py     # Testes unitários da Account
│   └── test\_transaction.py # Testes unitários da Transaction
│
├── .gitignore
└── README.md

````

---

## ⚡ Funcionalidades Atuais

- Gestão de contas com titular e saldo inicial
- Depósitos e saques com validações:
  - Limite máximo por saque
  - Número máximo de saques por conta
- Registro detalhado de transações via **Transaction**
- Geração de extrato completo da conta
- Validações e exceções:
  - Valores inválidos (zero ou negativos)
  - Saldo insuficiente
  - Limite de saques excedido

---

## 🧪 Testes

- Cobertura de operações válidas e inválidas
- Testes de exceções personalizadas
- Implementado com **pytest**
- **Executando os testes:**

```bash
pytest -v
````

> Cobertura completa será adicionada em versões futuras.

---

## 🛠 Tecnologias Utilizadas

* **Python 3.13**
* **pytest** (testes unitários)
* **Git / GitHub**
* Estrutura modular orientada a objetos
* Docstrings seguindo **PEP 257**

---

## 🚀 Roadmap / Próximas Implementações

O projeto está planejado para evoluir com:

1. **Extrato avançado**

   * Filtragem por tipo de transação ou período
   * Formatação em tabela e exportação CSV/JSON
2. **Transferências entre contas**

   * Validação de saldo
   * Registro de transações em ambas as contas
3. **Interface CLI ou GUI**

   * Menu interativo para usuário
   * Evolução futura para interface gráfica
4. **Persistência de dados**

   * Armazenamento em arquivos ou banco de dados
   * Histórico de transações completo
5. **Automação e integração**

   * API REST futura
   * Integração com sistemas de finanças externos
6. **Documentação e Licença**

   * Licença MIT a ser adicionada
   * Documentação detalhada das classes e métodos
7. **Versões futuras**

   * v1.1: Implementação de transferências
   * v1.2: Exportação de extrato
   * v2.0: Interface CLI completa

---

## 📌 Contatos e Suporte

* **Autor:** Gabriel Rodrigues
* **E-mail:** [gabrielhastec.dev@gmail.com](mailto:gabrielhastec.dev@gmail.com)
* **LinkedIn:** [linkedin.com/in/gabrielhastec](https://www.linkedin.com/in/gabrielhastec)

> Fique à vontade para abrir issues, sugerir melhorias ou contribuir com pull requests.

---

## ⚖ Licença

Este projeto é atualmente destinado a fins educacionais e demonstração de aprendizado pessoal.  
Embora não possua uma licença formal aplicada no momento, estou familiarizado com licenças de código aberto reconhecidas, como MIT, GPL e Apache.  

Planejo aplicar a licença MIT futuramente caso o projeto evolua para distribuição pública.  
Enquanto isso, o código pode ser estudado, adaptado e referenciado para fins de aprendizado, mas não deve ser usado em produção sem autorização.
