from typing import Optional, List
from bank.models.account import Account
from bank.models.transaction import Transaction
from bank.core.db import get_connection
from bank.exceptions import ContaNaoEncontradaError, ContaDuplicadaError
import sqlite3

"""Módulo que define a classe AccountRepository para persistência e consulta de contas e transações.

Fornece métodos para criar, consultar e atualizar contas e transações no banco de dados SQLite.
"""

class AccountRepository:
    """Classe para gerenciamento de persistência e consultas de contas e transações no banco de dados.

    Utiliza conexão SQLite para realizar operações de criação, leitura, atualização e gerenciamento
    de transações associadas a contas.
    """

    def create_account(self, cpf: str, name: str, balance: float = 0.0) -> Account:
        """Cria uma nova conta no banco de dados.

        Args:
            cpf (str): CPF do titular da conta.
            name (str): Nome do titular da conta.
            balance (float): Saldo inicial da conta (padrão 0.0).

        Returns:
            Account: Objeto Account representando a conta criada.

        Raises:
            ContaDuplicadaError: Se já existe uma conta com o mesmo CPF.
            sqlite3.OperationalError: Se houver um erro no banco de dados (ex.: tabela não existe).
        """
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO accounts (cpf, name, balance) VALUES (?, ?, ?)", (cpf, name, balance))
                conn.commit()
                account_id = cur.lastrowid
                return Account(id=account_id, cpf=cpf, name=name, balance=balance)
            except sqlite3.IntegrityError as e:
                # Detecta violação de UNIQUE no SQLite
                raise ContaDuplicadaError(f"Conta com CPF {cpf} já existe.") from e
            except sqlite3.OperationalError as e:
                # Propaga erro de tabela inexistente ou outros problemas operacionais
                raise sqlite3.OperationalError(f"Erro no banco de dados: {str(e)}") from e

    def get_account_by_id(self, account_id: int) -> Account:
        """Recupera uma conta do banco de dados pelo ID, incluindo suas transações.

        Args:
            account_id (int): Identificador único da conta.

        Returns:
            Account: Objeto Account com os dados da conta e suas transações.

        Raises:
            ContaNaoEncontradaError: Se a conta com o ID especificado não for encontrada.
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, cpf, name, balance FROM accounts WHERE id = ?", (account_id,))
            row = cur.fetchone()
            if not row:
                raise ContaNaoEncontradaError(f"Conta {account_id} não encontrada.")
            # Carregar transações
            cur.execute("SELECT id, account_id, type, amount, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp ASC", (account_id,))
            tx_rows = cur.fetchall()
            transactions = [Transaction(id=tx["id"], account_id=tx["account_id"], type=tx["type"], amount=tx["amount"], timestamp=tx["timestamp"]) for tx in tx_rows]
            return Account(id=row["id"], cpf=row["cpf"], name=row["name"], balance=row["balance"], transactions=transactions)

    def get_account_by_cpf(self, cpf: str) -> Optional[Account]:
        """Recupera uma conta do banco de dados pelo CPF.

        Args:
            cpf (str): CPF do titular da conta.

        Returns:
            Optional[Account]: Objeto Account se encontrado, None caso contrário.
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, cpf, name, balance FROM accounts WHERE cpf = ?", (cpf,))
            row = cur.fetchone()
            if not row:
                return None
            return self.get_account_by_id(row["id"])

    def update_balance(self, account_id: int, new_balance: float) -> None:
        """Atualiza o saldo de uma conta no banco de dados.

        Args:
            account_id (int): Identificador único da conta.
            new_balance (float): Novo saldo a ser definido.
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
            conn.commit()

    def add_transaction(self, account_id: int, type_: str, amount: float) -> int:
        """Adiciona uma nova transação ao banco de dados.

        Args:
            account_id (int): Identificador único da conta associada.
            type_ (str): Tipo da transação (ex.: 'deposit', 'withdraw').
            amount (float): Valor da transação.

        Returns:
            int: ID da transação recém-criada.
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (account_id, type_, amount))
            conn.commit()
            return cur.lastrowid

    def list_transactions(self, account_id: int) -> List[Transaction]:
        """Lista todas as transações de uma conta, ordenadas por data.

        Args:
            account_id (int): Identificador único da conta.

        Returns:
            List[Transaction]: Lista de objetos Transaction associados à conta.
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, account_id, type, amount, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp ASC", (account_id,))
            rows = cur.fetchall()
            return [Transaction(id=r["id"], account_id=r["account_id"], type=r["type"], amount=r["amount"], timestamp=r["timestamp"]) for r in rows]
