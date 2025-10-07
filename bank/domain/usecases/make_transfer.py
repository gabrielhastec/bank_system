from datetime import datetime
from bank.domain.entities.transaction import Transaction, TransactionType
from bank.interfaces.repositories.account_repo_interface import AccountRepositoryInterface
from bank.interfaces.repositories.transaction_repo_interface import TransactionRepositoryInterface
from bank.exceptions import ValorInvalidoError, SaldoInsuficienteError

"""
Caso de uso responsável por realizar transferências entre duas contas.
"""

class MakeTransferUseCase:
    """Caso de uso para transferir valores entre contas."""

    def __init__(self, account_repo: AccountRepositoryInterface, transaction_repo: TransactionRepositoryInterface):
        """Inicializa o caso de uso com os repositórios necessários."""
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def execute(self, source_account_id: int, destination_account_id: int, amount: float, description: str = None):
        """Executa a operação de transferência entre duas contas.

        Args:
            source_account_id (int): Conta de origem.
            destination_account_id (int): Conta de destino.
            amount (float): Valor da transferência.
            description (str, optional): Descrição da operação.

        Returns:
            tuple[Transaction, Transaction]: Transações de saída e entrada.
        """
        if source_account_id == destination_account_id:
            raise ValorInvalidoError("Contas de origem e destino não podem ser iguais.")

        # Busca as contas envolvidas na transferência
        source_account = self.account_repo.get_by_id(source_account_id)
        destination_account = self.account_repo.get_by_id(destination_account_id)

        if not source_account or not destination_account:
            raise ValorInvalidoError("Conta de origem ou destino não encontrada.")

        # Realiza a transferência
        source_account.withdraw_local(amount)
        destination_account.deposit_local(amount)

        # Atualiza ambas as contas no repositório
        self.account_repo.update(source_account)
        self.account_repo.update(destination_account)

        # Cria as transações correspondentes
        transaction_out = Transaction(
            id=self.transaction_repo.get_next_id(),
            account_id=source_account.id,
            type=TransactionType.TRANSFER_OUT.value,
            amount=amount,
            timestamp=datetime.utcnow(),
            description=description,
            related_account_id=destination_account.id
        )

        # Criação da transação de entrada
        transaction_in = Transaction(
            id=self.transaction_repo.get_next_id(),
            account_id=destination_account.id,
            type=TransactionType.TRANSFER_IN.value,
            amount=amount,
            timestamp=datetime.utcnow(),
            description=description,
            related_account_id=source_account.id
        )

        # Registro das transações
        self.transaction_repo.add(transaction_out)
        self.transaction_repo.add(transaction_in)

        return transaction_out, transaction_in
