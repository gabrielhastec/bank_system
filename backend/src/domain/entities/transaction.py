"""
Entidade Transaction
--------------------
Representa uma transação bancária no domínio da aplicação.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

from backend.src.domain.value_objects.money import Money

@dataclass(frozen=True, slots=True)
class Transaction:
    """Transação bancária."""

    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str
    type: str  # "deposit", "withdrawal", "transfer"
    amount: Money
    occurred_at: datetime
    description: Optional[str] = None

    @classmethod
    def create_deposit(cls, account_id: str, amount: Money, occurred_at: datetime = None) -> "Transaction":
        """Factory method para criar uma transação de depósito"""
        if occurred_at is None:
            occurred_at = datetime.utcnow()

        return cls(
            account_id=account_id,
            type="deposit",
            amount=amount,
            occurred_at=occurred_at,
            description=f"Depósito de {amount}"
        )

    @classmethod
    def create_withdrawal(cls, account_id: str, amount: Money, occurred_at: datetime = None) -> "Transaction":
        """Factory method para criar uma transação de saque"""
        if occurred_at is None:
            occurred_at = datetime.utcnow()
            
        return cls(
            account_id=account_id,
            type="withdrawal",
            amount=amount,
            occurred_at=occurred_at,
            description=f"Saque de {amount}"
        )

    @classmethod
    def create_transfer(cls, source_account_id: str, target_account_id: str, amount: Money) -> "Transaction":
        """Factory method para criar uma transação de transferência"""
        if occurred_at is None:
            occurred_at = datetime.utcnow()

        return cls(
            account_id=source_account_id,
            type="transfer",
            amount=amount,
            occurred_at=occurred_at,
            description=f"Transferência para conta {target_account_id[:8]}..."
        )
    