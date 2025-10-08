"""Gerenciamento de conexão com o banco de dados SQLite.

Este módulo fornece uma classe e um gerenciador de contexto para estabelecer e
gerenciar conexões com o banco de dados SQLite, utilizando configurações definidas
no módulo de configurações da aplicação bancária.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from bank.core.config.settings import settings

class DatabaseConnection:
    """Gerencia a conexão com o banco de dados SQLite.

    Responsável por inicializar, conectar e fechar conexões com o banco de dados
    utilizando o caminho especificado nas configurações.
    """
    def __init__(self, db_path: Path = settings.DB_PATH):
        """Inicializa a classe com o caminho do banco de dados.

        Args:
            db_path (Path): Caminho para o arquivo do banco de dados SQLite.
        """
        self.db_path = db_path
        self._connection = None

    def connect(self):
        """Cria e retorna uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Objeto de conexão com o banco de dados.
        """
        if not self._connection:
            self._connection = sqlite3.connect(self.db_path)
        return self._connection

    def close(self):
        """Fecha a conexão ativa com o banco de dados, se existir."""
        if self._connection:
            self._connection.close()
            self._connection = None

@contextmanager
def get_connection():
    """Fornece um contexto gerenciado para conexão com o banco de dados.

    Garante que a conexão seja aberta e fechada corretamente após o uso.

    Yields:
        sqlite3.Connection: Objeto de conexão com o banco de dados.
    """
    conn = DatabaseConnection().connect()
    try:
        yield conn
    finally:
        conn.close()
