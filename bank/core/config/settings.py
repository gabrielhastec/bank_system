"""Configurações globais da aplicação bancária.

Este módulo define as configurações principais da aplicação, incluindo nome,
modo de depuração, caminhos para banco de dados e logs, utilizando a biblioteca
Pydantic para validação e carregamento de variáveis de ambiente.
"""

from pydantic import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """Configurações principais da aplicação.

    Define variáveis de configuração como nome da aplicação, modo de depuração,
    caminhos para o banco de dados SQLite e configurações de logging.
    """
    APP_NAME: str = "Bank System"
    DEBUG: bool = True

    # Banco de dados SQLite local
    DB_NAME: str = "bank.db"
    DB_PATH: Path = BASE_DIR / "data" / DB_NAME

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = BASE_DIR / "logs" / "bank.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
