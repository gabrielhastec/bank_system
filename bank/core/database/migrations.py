"""Aplicação de migrações do banco de dados da aplicação bancária.

Este módulo contém a lógica para executar as migrações iniciais do banco de dados,
criando as tabelas definidas no esquema SQL utilizando uma conexão gerenciada.
"""

from bank.core.database.connection import get_connection
from bank.core.database.schema import SCHEMA_SQL
from bank.core.utils.logger import get_logger

logger = get_logger(__name__)

def apply_migrations():
    """Executa as migrações iniciais do banco de dados.

    Utiliza o esquema SQL definido para criar as tabelas necessárias e registra
    o progresso no logger.
    """
    logger.info("Iniciando migrações...")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript(SCHEMA_SQL)
        conn.commit()
    logger.info("Migrações aplicadas com sucesso.")
