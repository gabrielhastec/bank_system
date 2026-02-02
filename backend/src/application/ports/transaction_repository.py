"""
Porta de Repositório: ITransactionRepository
-------------------------------------------------
Define a interface que qualquer repositório de transações deve implementar.
"""

from abc import ABC, abstractmethod
from typing import List

from ...domain.entities.transaction import Transaction

class ITransactionRepository(ABC):
    """
    Interface para operações de persistência de transações.
    """

    @abstractmethod
    def save(self, transaction: Transaction) -> None:
        """Salva uma transação no banco de dados"""
        ...
    
    @abstractmethod
    def get_by_account_id(self, account_id: str) -> List[Transaction]:
        """Busca todas as transações de uma conta"""
        ...
    