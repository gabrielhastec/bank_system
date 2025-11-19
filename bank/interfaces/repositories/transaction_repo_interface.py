"""Interface para repositórios de transações financeiras.

Define um contrato (protocolo) para operações de manipulação de transações,
permitindo que casos de uso dependam de uma abstração em vez de implementações
concretas.
"""

from typing import Protocol, runtime_checkable, List, Optional, TYPE_CHECKING
from datetime import datetime
from bank.domain.exceptions import InvalidTransactionError, InvalidAmountError

if TYPE_CHECKING:
    from bank.domain.entities.transaction import Transaction

@runtime_checkable
class TransactionRepositoryInterface(Protocol):
    """Contrato para repositórios de transações financeiras."""
    def get_next_id(self) -> int:
        """Retorna o próximo identificador disponível para uma nova transação."""
        ...

    def add(self, transaction: "Transaction") -> None:
        """Persiste uma nova transação no repositório.

        Raises:
            InvalidTransactionError: se a transação for inválida (ex.: campos ausentes).
            InvalidAmountError: se o valor for inválido.
        """
        ...

    def find_by_account(self, account_id: int) -> List["Transaction"]:
        """Recupera todas as transações associadas a uma conta."""
        ...

    def get_by_id(self, transaction_id: int) -> Optional["Transaction"]:
        """Recupera uma transação pelo seu identificador."""
        ...

    def get_transactions_by_type_and_date_range(
        self,
        account_id: int,
        transaction_type: str,
        start_date: datetime,
        end_date: datetime
    ) -> List["Transaction"]:
        """Recupera transações de um tipo específico dentro de um intervalo de datas.

        Raises:
            InvalidAccountError: se a conta for inválida (implementação pode optar por lançar).
        """
        ...
