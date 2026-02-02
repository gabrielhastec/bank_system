
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class WithdrawDTO:
    """
    DTO para operação de saque.
    Transporta os dados necessários para realizar um saque.
    """
    account_id: str
    amount: str  # string para ser convertida em Money

    def __post_init__(self):
        # Validação básica: amount deve ser um número positivo
        try:
            amount_decimal = Decimal(self.amount)
            if amount_decimal <= 0:
                raise ValueError("O valor do saque deve ser positivo")
        except:
            raise ValueError("Valor inválido para saque")
        