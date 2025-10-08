"""Interface para repositórios de transações financeiras.

Define um contrato (protocolo) para operações de manipulação de transações,
permitindo que casos de uso dependam de uma abstração em vez de implementações
concretas.
"""

from typing import Protocol, runtime_checkable, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from bank.domain.entities.transaction import Transaction

@runtime_checkable
class TransactionRepositoryInterface(Protocol):
    """Contrato para repositórios de transações financeiras.

    Define métodos que implementações concretas devem seguir para gerenciar
    transações no sistema, garantindo compatibilidade com os casos de uso.
    """
    def get_next_id(self) -> int:
        """Retorna o próximo identificador disponível para uma nova transação.

        Returns:
            int: Próximo identificador disponível (não persiste a transação).
        """
        ...

    def add(self, transaction: "Transaction") -> None:
        """Persiste uma nova transação no repositório.

        Args:
            transaction (Transaction): Instância da transação a ser persistida.
        """
        ...

    def find_by_account(self, account_id: int) -> List["Transaction"]:
        """Recupera todas as transações associadas a uma conta.

        Args:
            account_id (int): Identificador da conta cujas transações serão recuperadas.

        Returns:
            List[Transaction]: Lista de transações associadas à conta.
        """
        ...

    def get_by_id(self, transaction_id: int) -> Optional["Transaction"]:
        """Recupera uma transação pelo seu identificador.

        Args:
            transaction_id (int): Identificador da transação a ser recuperada.

        Returns:
            Optional[Transaction]: Instância da transação se encontrada, ou None se não existir.
        """
        ...
