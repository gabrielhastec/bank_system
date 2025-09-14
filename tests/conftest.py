import pytest
import tempfile
import os
from bank.core import db, schema

"""
Módulo de configuração de testes para o sistema bancário.

Define uma fixture do pytest para criar e gerenciar um banco de dados SQLite temporário
isolado para cada teste, garantindo um ambiente limpo e independente.
"""

@pytest.fixture(autouse=True, scope="function")

def tmp_db(monkeypatch) -> None:
    """Cria um banco de dados SQLite temporário para cada teste.

    Configura um arquivo temporário para o banco de dados, inicializa o esquema
    usando create_tables e remove o arquivo após o teste.

    Args:
        monkeypatch: Objeto do pytest para modificar atributos dinamicamente.

    Yields:
        None: A fixture cede o controle após configurar o banco temporário.

    Note:
        O arquivo temporário é excluído automaticamente após cada teste.
    """
    # Cria um banco em arquivo temporário isolado por teste
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    monkeypatch.setattr(db, "DB_FILE", tmp.name)
    # Inicializa o schema no DB temporário
    schema.create_tables()
    yield
    os.unlink(tmp.name)
    