
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):

    # Banco de dados
    database_url: str = "sqlite:///./data/bank.db"
    bcrypt_rounds: int = 12

    # JWT
    jwt_secret_key: str = "8519"  # Adicionar
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24  # 24 horas
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"

settings = Settings()
