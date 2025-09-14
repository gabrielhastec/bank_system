import pytest
from bank.core import db, schema

"""
Módulo de configuração de testes para o sistema bancário.

Define uma fixture do pytest para criar e gerenciar um banco de dados SQLite em memória
isolado para cada teste, garantindo um ambiente limpo e independente.
"""

@pytest.fixture(autouse=True, scope="function")
def tmp_db(monkeypatch) -> None:
    """Cria um banco de dados SQLite em memória para cada teste.

    Configura um banco de dados em memória, inicializa o esquema usando create_tables
    e descarta o banco após o teste.

    Args:
        monkeypatch: Objeto do pytest para modificar atributos dinamicamente.

    Yields:
        None: A fixture cede o controle após configurar o banco em memória.

    Note:
        O banco em memória é descartado automaticamente após cada teste, eliminando
        a necessidade de gerenciar arquivos físicos.
    """
    
    # Configura banco em memória
    monkeypatch.setattr(db, "DB_FILE", ":memory:")
    
    # Inicializa o schema
    try:
        schema.create_tables()
        # Verifica se a tabela accounts foi criada
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
            if not cur.fetchone():
                raise RuntimeError("Tabela 'accounts' não foi criada.")
    except Exception as e:
        raise RuntimeError(f"Falha ao inicializar o schema: {str(e)}") from e
    yield
    # Banco em memória é descartado automaticamente, sem necessidade de exclusão
