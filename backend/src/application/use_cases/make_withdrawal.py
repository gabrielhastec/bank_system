
from dataclasses import dataclass
from datetime import datetime

from ...domain.aggregates.account import Account
from ...domain.value_objects.money import Money
from ..ports.account_repository import IAccountRepository
from ..ports.transaction_repository import ITransactionRepository

@dataclass
class WithdrawalCommand:
    account_id: str
    amount: str

class MakeWithdrawalUseCase:
    def __init__(self, account_repo: IAccountRepository, transaction_repo: ITransactionRepository):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def execute(self, command: WithdrawalCommand):
        account = self.account_repo.get_by_id(command.account_id)
        if not account:
            raise ValueError("Conta não encontrada")
        
        amount = Money(command.amount)
        occurred_at = datetime.utcnow()
        transaction = account.withdraw(amount, occurred_at)
        self.account_repo.save(account)
        self.transaction_repo.save(transaction)
        return account
