# Sistema Bancário - Clean Architecture

## 📋 Visão Geral

Sistema bancário digital implementado seguindo os princípios da **Clean Architecture** (Arquitetura Limpa), com separação clara de responsabilidades entre camadas de domínio, aplicação, infraestrutura e interface.

### 🎯 Objetivo
Fornecer uma base sólida e escalável para operações bancárias (abertura de contas, transações, consultas) com foco em:
- **Manutenibilidade**: Código organizado e de fácil compreensão
- **Testabilidade**: Dependências invertidas e isoladas
- **Flexibilidade**: Fácil substituição de componentes (ex: banco de dados, serviços externos)

## 🏗️ Arquitetura

```
Clean Architecture Layers:
┌─────────────────────────────────────┐
│          Interface (API/CLI)        │ ← Recebe requisições externas
├─────────────────────────────────────┤
│         Application Layer           │ ← Orquestra casos de uso
├─────────────────────────────────────┤
│           Domain Layer              │ ← Regras de negócio puras
├─────────────────────────────────────┤
│       Infrastructure Layer          │ ← Detalhes técnicos (DB, serviços)
└─────────────────────────────────────┘
```

### Camadas Implementadas

#### 1. **Domínio (Domain Layer)**
- **Entidades**: `Customer`, `Account` (aggregate root)
- **Value Objects**: `CPF`, `Money`, `Password`
- **Exceções**: `InsufficientFunds`, `DailyLimitExceeded`, `DuplicateCPFException`
- **Regras de negócio**: Limites diários, validação de CPF, criptografia de senha

#### 2. **Aplicação (Application Layer)**
- **Casos de uso**: `OpenAccountUseCase`, `MakeDepositUseCase`
- **DTOs**: `OpenAccountDTO`, `DepositCommand`
- **Portas (Interfaces)**: `IAccountRepository`, `ICustomerRepository`, `INotificationService`

#### 3. **Infraestrutura (Infrastructure Layer)**
- **Repositórios**: `AccountRepositorySQLite`, `CustomerRepositorySQLite`
- **Serviços**: `ConsoleNotificationService`, `HashingService`
- **ORM**: SQLModel com SQLite
- **Container**: Injeção de dependências com `dependency_injector`

#### 4. **Interface (Interface Layer)**
- **API REST**: FastAPI com schemas Pydantic
- **CLI**: Interface de linha de comando para testes

## 🚀 Funcionalidades Atuais

### ✅ Implementadas
- [x] Abertura de conta bancária
- [x] Validação de CPF
- [x] Hash de senha com bcrypt
- [x] Persistência em SQLite
- [x] API REST para criação de contas
- [x] CLI interativa para abertura de conta
- [x] Injeção de dependências automatizada
- [x] Regras de domínio (limites, saldo)

### 🔄 Em Desenvolvimento
- [ ] Depósitos
- [ ] Saques
- [ ] Transferências
- [ ] Extrato bancário
- [ ] Autenticação JWT
- [ ] Frontend React
- [ ] Dockerização completa

## 📁 Estrutura do Projeto

```
backup/
├── backend/                    # API Principal
│   ├── src/
│   │   ├── api/               # FastAPI (Controllers)
│   │   ├── application/       # Casos de Uso e DTOs
│   │   ├── domain/            # Regras de Negócio
│   │   ├── infrastructure/    # Implementações Técnicas
│   │   └── shared/            # Utilitários
│   ├── Dockerfile
│   └── pyproject.toml
├── cli/                       # Interface de Linha de Comando
│   └── main.py
├── frontend/                  # Futura Interface Web
│   └── src/
├── docker-compose.yml
└── requirements.txt
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **FastAPI**: Framework web moderno
- **SQLModel**: ORM com tipos Python
- **Pydantic**: Validação de dados
- **Dependency Injector**: Injeção de dependências
- **Passlib**: Criptografia de senhas

### Banco de Dados
- **SQLite** (desenvolvimento) - pronto para PostgreSQL/MySQL

### Frontend (Planejado)
- **React 18** com Vite
- **Tailwind CSS**
- **Axios** para chamadas HTTP

## ⚡ Como Executar

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <repositorio>
cd backup
```

2. **Configure o ambiente Python**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Inicialize o banco de dados**
```bash
python -c "from backend.src.infrastructure.database.orm import init_db; init_db()"
```

5. **Execute a API**
```bash
cd backend
uvicorn src.api.main:app --reload
```
API disponível em: http://localhost:8000
Documentação: http://localhost:8000/docs

6. **Teste a CLI**
```bash
cd cli
python main.py
```

## 📊 Endpoints da API

### POST /accounts/
Abre uma nova conta bancária.

**Request:**
```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "cpf": "12345678900",
  "password": "senha123"
}
```

**Response (201):**
```json
{
  "account_id": "uuid-da-conta",
  "name": "João Silva",
  "cpf": "123.456.789-00"
}
```

## 🧪 Testando com a CLI

A CLI oferece interface interativa para testes:
```bash
=== Banco Digital - Abertura de Conta ===

Nome completo: Maria Santos
Email: maria@email.com
CPF (somente números): 98765432100
Senha (mínimo 6 caracteres): minhasenha

SUCESSO! Conta criada com sucesso!
Número da conta: a1b2c3d4-e5f6-...
Titular: Maria Santos
Email: maria@email.com
CPF: 987.654.321-00
Saldo inicial: R$ 0,00
```

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do backend:
```env
DATABASE_URL=sqlite:///./data/bank.db
BCRYPT_ROUNDS=12
```

### Banco de Dados
- Local: `./data/bank.db`
- Migrações automáticas na inicialização
- Modelos: `AccountModel`, `CustomerModel`, `TransactionModel`

## 📝 Convenções de Código

### Documentação
- **Docstrings** seguindo PEP 257
- **Type hints** em todas as funções
- **Comentários** explicativos para lógica complexa

### Estrutura
- **Camadas isoladas**: Domínio não conhece infraestrutura
- **Inversão de dependência**: Interfaces → Implementações
- **Imutabilidade**: Value Objects são frozen dataclasses

### Padrões
- **DTOs** para transferência entre camadas
- **Factory Methods** para criação de entidades
- **Aggregate Root** para transações consistentes

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro ao criar conta com CPF existente**
```
ValueError: CPF já cadastrado no sistema.
```
Solução: Use um CPF diferente ou limpe o banco de dados.

2. **Senha muito curta**
```
ValueError: Password must be at least 6 characters
```
Solução: Use senhas com 6+ caracteres.

3. **CPF inválido**
```
ValueError: CPF inválido
```
Solução: Use CPF válido (11 dígitos, dígitos verificadores corretos).

### Limpeza do Banco
```bash
rm -rf data/
python -c "from backend.src.infrastructure.database.orm import init_db; init_db()"
```

## 🚧 Próximos Passos

### Prioridade Alta
1. Implementar autenticação JWT
2. Completar operações (saque, depósito, transferência)
3. Criar extrato bancário

### Prioridade Média
1. Frontend React completo
2. Dockerização
3. Testes unitários e de integração
4. Logging estruturado

### Melhorias Futuras
1. Migração para PostgreSQL
2. Sistema de filas para notificações
3. Cache com Redis
4. Monitoramento com Prometheus

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 👥 Autores

- **Equipe de Desenvolvimento** - Implementação inicial
- **Contribuidores** - Lista de colaboradores

## 📞 Suporte

Para suporte, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.
