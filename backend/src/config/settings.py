

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/bank.db"
    bcrypt_rounds: int = 12
    
settings = Settings()
