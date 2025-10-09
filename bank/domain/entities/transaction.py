from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum
from bank.utils.validators import ensure_positive_number
from bank.exceptions import ValorInvalidoError

"""Módulo que define a classe Transaction para representar transações financeiras.

A classe Transaction armazena informações sobre uma transação, como identificador,
conta associada, tipo, valor e carimbo de data/hora, para uso em sistemas de gerenciamento
de contas.
"""

class TransactionType(Enum):
    """Enumeração dos tipos de transações financeiras.

    Tipos possíveis:
        DEPOSIT: Depósito de dinheiro na conta.
        WITHDRAW: Retirada de dinheiro
    """
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"

@dataclass(frozen=True)
class Transaction:
    """Classe que representa uma transação financeira.

    Atributos:
        id (Optional[int]): Identificador único da transação, None se não persistida.
        account_id (int): Identificador da conta associada à transação.
        type (str): Tipo da transação (ex.: 'deposit', 'withdraw').
        amount (float): Valor da transação.
        timestamp (Optional[datetime]): Data e hora da transação, None se não definida.
    """
    id: Optional[int]
    account_id: int
    type: str
    amount: float
    timestamp: Optional[datetime] = None
    description: Optional[str] = None
    related_account_id: Optional[int] = None
    
    def __post_init__(self):
        """Valida os atributos após a inicialização do dataclass.
        Levanta ValueError se o tipo de transação for inválido.

        Args:
            None
        """   
        if not isinstance(self.type, str) or self.type not in [t.value for t in TransactionType]:
            raise ValueError(f"Tipo de transação inválido: {self.type}. Use: {[t.value for t in TransactionType]}")
        
        # Garantir que o valor seja positivo
        object.__setattr__(self, "amount", ensure_positive_number(self.amount))
        if self.account_id <= 0:
            raise ValorInvalidoError("ID da conta deve ser positivo.")
        if self.related_account_id is not None and self.related_account_id <= 0:
            raise ValorInvalidoError("ID da conta relacionada deve ser positivo.")
        
        # Definir timestamp atual se não fornecido
        if self.timestamp is None:
            object.__setattr__(self, "timestamp", datetime.utcnow())

    def as_dict(self) -> dict:
        """Converte a instância da transação em um dicionário.
        
        Returns:
            dict: Dicionário com os atributos da transação.
        """
        return {
            "id": self.id,
            "account_id": self.account_id,
            "type": self.type,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "description": self.description,
            "related_account_id": self.related_account_id
        }
