import sqlite3
from pathlib import Path

"""Módulo para gerenciamento da conexão com o banco de dados SQLite.

Define caminhos para o arquivo de banco de dados e fornece uma função para obter
uma conexão SQLite configurada com autocommit e suporte a tipos personalizados.
"""

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "bank.db"

def get_connection() -> sqlite3.Connection:
    """Retorna uma conexão SQLite configurada para o banco de dados.

    A conexão é configurada com suporte a tipos personalizados (PARSE_DECLTYPES e
    PARSE_COLNAMES) e utiliza o modo row_factory para acessar colunas por nome.
    O autocommit é gerenciado via contexto.

    Returns:
        sqlite3.Connection: Conexão ativa com o banco de dados.
    """
    conn = sqlite3.connect(
        DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    conn.row_factory = sqlite3.Row
    return conn
