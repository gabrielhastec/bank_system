"""Repositório SQLite para manipulação de usuários.

Fornece métodos para operações CRUD (criar e recuperar) no banco de dados SQLite
para usuários, utilizando uma conexão gerenciada e logger adaptado.
"""

from bank.core.database.connection import get_connection
from bank.infrastructure.utils.logger_adapter import LoggerAdapter

logger = LoggerAdapter(__name__)

class UserRepositorySQLite:
    """Gerencia operações CRUD para usuários no banco de dados SQLite.

    Implementa métodos para criação e recuperação de usuários, utilizando uma
    conexão gerenciada com o banco SQLite.
    """
    def create(self, name: str, email: str, password: str) -> int:
        """Cria um novo usuário no banco de dados.

        Args:
            name (str): Nome do usuário.
            email (str): Endereço de e-mail do usuário.
            password (str): Senha do usuário.

        Returns:
            int: Identificador do usuário criado.
        """
        query = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, email, password))
            conn.commit()
            logger.info(f"Usuário criado: {name} ({email})")
            return cursor.lastrowid

    def get_by_email(self, email: str) -> tuple | None:
        """Recupera um usuário pelo seu endereço de e-mail.

        Args:
            email (str): Endereço de e-mail do usuário a ser recuperado.

        Returns:
            tuple | None: Tupla com os dados do usuário (id, name, email, password,
                created_at) se encontrado, ou None se não encontrado.
        """
        query = "SELECT id, name, email, password, created_at FROM users WHERE email = ?"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            return cursor.fetchone()
        