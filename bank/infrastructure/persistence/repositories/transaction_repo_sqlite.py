"""Repositório SQLite para manipulação de transações financeiras.

Fornece métodos para criar e recuperar transações financeiras no banco de dados
SQLite, utilizando modelos de persistência e logger adaptado.
"""

from bank.core.database.connection import get_connection
from bank.infrastructure.persistence.models.transaction_model import TransactionModel
from bank.infrastructure.utils.logger_adapter import LoggerAdapter

logger = LoggerAdapter(__name__)

class TransactionRepositorySQLite:
    """Gerencia operações CRUD para transações financeiras no banco SQLite.

    Implementa métodos para criação e recuperação de transações, utilizando uma
    conexão gerenciada com o banco SQLite.
    """
    def create(self, account_id: int, amount: float, type: str) -> int:
        """Cria uma nova transação financeira no banco de dados.

        Args:
            account_id (int): Identificador da conta associada à transação.
            amount (float): Valor da transação.
            type (str): Tipo da transação (ex.: depósito, saque).

        Returns:
            int: Identificador da transação criada.
        """
        query = "INSERT INTO transactions (account_id, amount, type) VALUES (?, ?, ?)"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (account_id, amount, type))
            conn.commit()
            logger.info(f"Transação registrada: conta {account_id}, tipo {type}, valor {amount}")
            return cursor.lastrowid

    def get_by_account(self, account_id: int) -> list[TransactionModel]:
        """Recupera todas as transações associadas a uma conta.

        Args:
            account_id (int): Identificador da conta cujas transações serão recuperadas.

        Returns:
            list[TransactionModel]: Lista de modelos de transação associados à conta.
        """
        query = "SELECT id, account_id, amount, type, created_at FROM transactions WHERE account_id = ?"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (account_id,))
            rows = cursor.fetchall()
            return [TransactionModel.from_row(row) for row in rows]
        