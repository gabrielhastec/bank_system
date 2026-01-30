from pydantic import BaseModel
from decimal import Decimal

class DepositRequest(BaseModel):
    amount: Decimal

class WithdrawRequest(BaseModel):
    amount: Decimal

class TransferRequest(BaseModel):
    target_account_id: str
    amount: Decimal

class TransactionResponse(BaseModel):
    transaction_id: str
    type: str
    amount: Decimal
    occurred_at: str

class StatementResponse(BaseModel):
    transactions: list[TransactionResponse]
    