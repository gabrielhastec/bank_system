
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DepositDTO:
    """
    DTO para operação de depósito.
    Transporta os dados necessários para realizar um depósito.
    """
    account_id: str
    amount: str  # string para ser convertida em Money

    def __post_init__(self):
        # Validação básica: amount deve ser um número positivo
        try:
            amount_decimal = Decimal(self.amount)
            if amount_decimal <= 0:
                raise ValueError("O valor do depósito deve ser positivo")
        except:
            raise ValueError("Valor inválido para depósito")
        