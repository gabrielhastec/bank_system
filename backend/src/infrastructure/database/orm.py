
from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

from .models.account_model import AccountModel
from .models.transaction_model import TransactionModel  # importar o novo modelo

DATABASE_URL = "sqlite:///./data/bank.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    Path("./data").mkdir(exist_ok=True)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    init_db()