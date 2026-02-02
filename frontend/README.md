# Frontend - Sistema Bancário

## 🚀 Como Executar

### Pré-requisitos
- Node.js 16+ e npm/yarn
- Backend em execução (http://localhost:8000)

### Instalação
```bash
cd frontend
npm install
```

### Execução em Desenvolvimento
```bash
npm start
```
- Acesse: http://localhost:3000

### Build para Produção
```bash
npm run build
```

## 📁 Estrutura do Projeto

```text
src/
├── components/         # Componentes reutilizáveis
├── pages/             # Páginas da aplicação
├── services/          # Serviços de API
├── hooks/             # Hooks customizados
├── utils/             # Utilitários
└── App.jsx           # Componente principal
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo .env na raiz do frontend:
```env
REACT_APP_API_URL=http://localhost:8000
```

## 📋 Funcionalidades

- Criação de conta
- Login com CPF e senha
- Dashboard com saldo
- Depósito
- Saque
- Transferência
- Extrato de transações
- Responsividade

## 🛠️ Tecnologias

- React 18 com hooks
- React Router DOM 6 para navegação
- Axios para requisições HTTP
- React Hook Form para formulários
- Zod para validação
- React Query para cache e estado
- Tailwind CSS para estilização
- React Hot Toast para notificações
