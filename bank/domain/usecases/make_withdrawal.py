from datetime import datetime
from bank.domain.entities.transaction import Transaction, TransactionType
from bank.interfaces.repositories.account_repo_interface import AccountRepositoryInterface
from bank.interfaces.repositories.transaction_repo_interface import TransactionRepositoryInterface
from bank.domain.exceptions import (
    InsufficientFundsError,
    DailyLimitExceededError,
    InvalidAccountError,
    InvalidAmountError
)

"""
Caso de uso responsável por realizar saques em uma conta bancária.
"""

class MakeWithdrawalUseCase:
    """Caso de uso para realizar saque de uma conta."""
    MAX_DAILY_WITHDRAWALS = 10  # Limite máximo de saques diários

    def __init__(self, account_repo: AccountRepositoryInterface, transaction_repo: TransactionRepositoryInterface):
        """Inicializa o caso de uso com os repositórios necessários."""
        
        # Inicialização dos repositórios
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def execute(self, account_id: int, amount: float, description: str = None) -> Transaction:
        """Executa a operação de saque.

        Args:
            account_id (int): Identificador da conta.
            amount (float): Valor a ser sacado.
            description (str, optional): Descrição da operação.

        Returns:
            Transaction: Transação registrada.
        """
        
        # Busca a conta
        account = self.account_repo.get_by_id(account_id)
        if not account:
            raise InvalidAccountError(f"Conta com ID {account_id} não encontrada.")
        
        # Verifica se o valor do saque é válido
        if amount <= 0:
            raise InvalidAmountError(f"Valor do saque deve ser maior que zero. Valor fornecido: {amount}")

        # Verifica se há saldo suficiente
        if account.balance < amount:
            raise InsufficientFundsError(account.balance, amount)

        # Verifica se o limite diário de saques foi excedido
        if account.get_daily_withdrawals() >= self.MAX_DAILY_WITHDRAWALS:
            raise DailyLimitExceededError(
                account_id=account_id,
                limit=self.MAX_DAILY_WITHDRAWALS,
                next_allowed_date_iso=account.get_next_allowed_date_iso()
            )

        # Realiza o saque
        account.withdraw_local(amount)
        self.account_repo.update(account)

        # Cria a transação de saque 
        transaction = Transaction(
            id=self.transaction_repo.get_next_id(),
            account_id=account.id,
            type=TransactionType.WITHDRAW.value,
            amount=amount,
            timestamp=datetime.utcnow(),
            description=description
        )

        # Registra a transação
        self.transaction_repo.add(transaction)
        return transaction
