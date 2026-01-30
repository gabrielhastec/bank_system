
from sqlmodel import SQLModel, Field

from decimal import Decimal
from datetime import datetime
from typing import Optional

class TransactionModel(SQLModel, table=True):
    transaction_id: str = Field(primary_key=True)
    account_id: str = Field(foreign_key="accountmodel.account_id", index=True)
    type: str  # deposit, withdrawal, transfer
    amount: Decimal = Field(decimal_places=2, max_digits=12)
    occurred_at: datetime
    # Para transferências, podemos adicionar campo de conta destino
    target_account_id: Optional[str] = None
