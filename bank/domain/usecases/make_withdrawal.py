from datetime import datetime
from bank.domain.entities.transaction import Transaction, TransactionType
from bank.interfaces.repositories.account_repo_interface import AccountRepositoryInterface
from bank.interfaces.repositories.transaction_repo_interface import TransactionRepositoryInterface
from bank.exceptions import ValorInvalidoError, SaldoInsuficienteError

"""
Caso de uso responsável por realizar saques em uma conta bancária.
"""

class MakeWithdrawalUseCase:
    """Caso de uso para realizar saque de uma conta."""

    def __init__(self, account_repo: AccountRepositoryInterface, transaction_repo: TransactionRepositoryInterface):
        """Inicializa o caso de uso com os repositórios necessários."""
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
        # Validação do valor do saque
        account = self.account_repo.get_by_id(account_id)
        if not account:
            raise ValorInvalidoError("Conta não encontrada.")

        # Verifica se há saldo suficiente
        account.withdraw_local(amount)
        self.account_repo.update(account)

        # Criação da transação de saque
        transaction = Transaction(
            id=self.transaction_repo.get_next_id(),
            account_id=account.id,
            type=TransactionType.WITHDRAW.value,
            amount=amount,
            timestamp=datetime.utcnow(),
            description=description
        )

        # Registro da transação
        self.transaction_repo.add(transaction)
        return transaction
