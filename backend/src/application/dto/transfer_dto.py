
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class TransferDTO:
    """
    DTO para operação de transferência.
    Transporta os dados necessários para realizar uma transferência.
    """
    source_account_id: str
    target_account_id: str
    amount: str  # string para ser convertida em Money

    def __post_init__(self):
        # Validação básica: amount deve ser um número positivo
        try:
            amount_decimal = Decimal(self.amount)
            if amount_decimal <= 0:
                raise ValueError("O valor da transferência deve ser positivo")
            if self.source_account_id == self.target_account_id:
                raise ValueError("Não é possível transferir para a mesma conta")
        except:
            raise ValueError("Valor inválido para transferência")
        