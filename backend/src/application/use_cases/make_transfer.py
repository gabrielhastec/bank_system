
from dataclasses import dataclass
from datetime import datetime

from ...domain.aggregates.account import Account
from ...domain.value_objects.money import Money
from ..ports.account_repository import IAccountRepository
from ..ports.transaction_repository import ITransactionRepository

@dataclass
class TransferCommand:
    source_account_id: str
    target_account_id: str
    amount: str

class MakeTransferUseCase:
    def __init__(self, account_repo: IAccountRepository, transaction_repo: ITransactionRepository):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def execute(self, command: TransferCommand):
        source = self.account_repo.get_by_id(command.source_account_id)
        target = self.account_repo.get_by_id(command.target_account_id)
        
        if not source or not target:
            raise ValueError("Conta de origem ou destino não encontrada")
        
        amount = Money(command.amount)
        occurred_at = datetime.utcnow()
        
        # Realizar a transferência: debitar da origem e creditar no destino
        withdrawal_transaction = source.withdraw(amount, occurred_at)
        deposit_transaction = target.deposit(amount, occurred_at)
        
        self.account_repo.save(source)
        self.account_repo.save(target)
        self.transaction_repo.save(withdrawal_transaction)
        self.transaction_repo.save(deposit_transaction)
        
        return source
