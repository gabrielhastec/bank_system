from .db import get_connection

"""Módulo para inicialização do esquema do banco de dados.

Define a função create_tables para criar as tabelas accounts e transactions
no banco de dados SQLite, com as respectivas chaves primárias, chaves estrangeiras
e restrições de integridade.
"""

def create_tables() -> None:
    """Cria as tabelas accounts e transactions no banco de dados, se não existirem.

    A tabela accounts armazena informações de contas, incluindo ID, CPF, nome e saldo.
    A tabela transactions registra transações associadas a contas, com ID, ID da conta,
    tipo, valor e carimbo de data/hora. O autocommit é gerenciado via contexto.

    Note:
        - A tabela accounts possui uma restrição UNIQUE no campo cpf.
        - A tabela transactions possui uma chave estrangeira referenciando accounts(id).
        - O campo timestamp em transactions usa CURRENT_TIMESTAMP como padrão.
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )""")
        conn.commit()
