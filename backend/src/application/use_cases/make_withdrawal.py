
from dataclasses import dataclass
from datetime import datetime

from ...domain.aggregates.account import Account
from ..ports.account_repository import IAccountRepository
from ...domain.value_objects.money import Money

@dataclass
class WithdrawalCommand:
    account_id: str
    amount: str

class MakeWithdrawalUseCase:
    def __init__(self, account_repo: IAccountRepository):
        self.account_repo = account_repo

    def execute(self, command: WithdrawalCommand):
        account = self.account_repo.get_by_id(command.account_id)
        if not account:
            raise ValueError("Conta não encontrada")
        
        amount = Money(command.amount)
        account.withdraw(amount, datetime.utcnow())
        self.account_repo.save(account)
        return account
