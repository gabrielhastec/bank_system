from dataclasses import dataclass
from datetime import datetime
from typing import Optional

"""Módulo que define a classe Transaction para representar transações financeiras.

A classe Transaction armazena informações sobre uma transação, como identificador,
conta associada, tipo, valor e carimbo de data/hora, para uso em sistemas de gerenciamento
de contas.
"""

@dataclass
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