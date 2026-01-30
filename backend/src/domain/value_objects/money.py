

from decimal import Decimal
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal

    ZERO = Decimal("0.00")

    def __init__(self, amount: str | float | Decimal | int):
        if isinstance(amount, str):
            amount = Decimal(amount.replace(",", "."))
        elif isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        object.__setattr__(self, "amount", amount.quantize(Decimal("0.01")))

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __sub__(self, other: "Money") -> "Money":
        return Money(self.amount - other.amount)

    def __lt__(self, other: "Money") -> bool:
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        return self.amount <= other.amount

    def __repr__(self) -> str:
        return f"R${self.amount:.2f}".replace(".", ",")
    