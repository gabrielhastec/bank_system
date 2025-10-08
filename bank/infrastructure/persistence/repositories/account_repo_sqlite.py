"""Repositório SQLite para manipulação de contas bancárias.

Fornece métodos para operações CRUD (criar, recuperar e atualizar) no banco de
dados SQLite para contas bancárias, utilizando modelos de persistência e logger
adaptado.
"""

from bank.core.database.connection import get_connection
from bank.infrastructure.persistence.models.account_model import AccountModel
from bank.infrastructure.utils.logger_adapter import LoggerAdapter

logger = LoggerAdapter(__name__)

class AccountRepositorySQLite:
    """Gerencia operações CRUD para contas no banco de dados SQLite.

    Implementa métodos para criação, recuperação e atualização de contas,
    utilizando uma conexão gerenciada com o banco SQLite.
    """
    def create(self, user_id: int, balance: float = 0.0) -> int:
        """Cria uma nova conta para um usuário no banco de dados.

        Args:
            user_id (int): Identificador do usuário associado à conta.
            balance (float, optional): Saldo inicial da conta. Padrão é 0.0.

        Returns:
            int: Identificador da conta criada.
        """
        query = "INSERT INTO accounts (user_id, balance) VALUES (?, ?)"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, balance))
            conn.commit()
            logger.info(f"Conta criada para usuário {user_id}")
            return cursor.lastrowid

    def get_by_id(self, account_id: int) -> AccountModel | None:
        """Recupera uma conta pelo seu identificador.

        Args:
            account_id (int): Identificador da conta a ser recuperada.

        Returns:
            AccountModel | None: Instância do modelo de conta se encontrada, ou None
                se a conta não existir.
        """
        query = "SELECT id, user_id, balance FROM accounts WHERE id = ?"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (account_id,))
            row = cursor.fetchone()
            return AccountModel.from_row(row) if row else None

    def update_balance(self, account_id: int, new_balance: float) -> None:
        """Atualiza o saldo de uma conta no banco de dados.

        Args:
            account_id (int): Identificador da conta a ser atualizada.
            new_balance (float): Novo valor do saldo.
        """
        query = "UPDATE accounts SET balance = ? WHERE id = ?"
        with get_connection() as conn:
            conn.execute(query, (new_balance, account_id))
            conn.commit()
            logger.info(f"Saldo atualizado para a conta {account_id}: {new_balance}")
