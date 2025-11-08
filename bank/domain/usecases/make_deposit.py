from datetime import datetime
from bank.domain.entities.transaction import Transaction, TransactionType
from bank.interfaces.repositories.account_repo_interface import AccountRepositoryInterface
from bank.interfaces.repositories.transaction_repo_interface import TransactionRepositoryInterface
from bank.domain.exceptions import ( 
    InvalidAmountError,
    InvalidAccountError
)

"""
Caso de uso responsável por realizar depósitos em uma conta bancária.
"""

class MakeDepositUseCase:
    """Caso de uso para realizar depósito em conta."""

    def __init__(self, account_repo: AccountRepositoryInterface, transaction_repo: TransactionRepositoryInterface):
        """Inicializa o caso de uso com os repositórios necessários."""
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def execute(self, account_id: int, amount: float, description: str = None) -> Transaction:
        """Executa a operação de depósito.

        Args:
            account_id (int): Identificador da conta.
            amount (float): Valor do depósito.
            description (str, optional): Descrição da operação.

        Returns:
            Transaction: Transação registrada.
        """
        # Validação do valor do depósito
        account = self.account_repo.get_by_id(account_id)
        if not account:
            raise InvalidAccountError(f"Conta com ID {account_id} não encontrada.")
        
        # Verifica se o valor do depósito é válido
        if amount <= 0:
            raise InvalidAmountError(f"Valor do depósito deve ser maior que zero. Valor fornecido: {amount}")

        # Deposita o valor na conta
        self.account_repo.update(account)
        
        # Cria a transação de depósito
        transaction = Transaction(
            id=self.transaction_repo.get_next_id(),
            account_id=account.id,
            type=TransactionType.DEPOSIT.value,
            amount=amount,
            timestamp=datetime.utcnow(),
            description=description
        )

        # Registra a transação
        self.transaction_repo.add(transaction)
        return transaction
