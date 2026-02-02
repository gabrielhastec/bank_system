"""
Configurações de testes para pytest.
"""

import pytest
import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from infrastructure.database.orm import init_db, engine
from sqlmodel import Session

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Configura o banco de dados para testes.
    Executado uma vez por sessão de testes.
    """
    # Usa banco de dados em memória para testes
    global engine
    engine = create_engine("sqlite:///:memory:", echo=False)
    
    # Cria todas as tabelas
    init_db()
    yield
    # Limpeza após os testes
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def db_session():
    """
    Fornece uma sessão do banco de dados para cada teste.
    """
    with Session(engine) as session:
        yield session
        session.rollback()
        