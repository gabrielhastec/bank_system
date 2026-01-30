

from dataclasses import dataclass
from datetime import datetime
from ...domain.aggregates.account import Account
from ..ports.account_repository import IAccountRepository
from ...domain.value_objects.money import Money

@dataclass
class DepositCommand:
    account_id: str
    amount: str  # vem como string do front

class MakeDepositUseCase:
    def __init__(self, account_repo: IAccountRepository):
        self.account_repo = account_repo

    def execute(self, command: DepositCommand):
        account = self.account_repo.get_by_id(command.account_id)
        if not account:
            raise ValueError("Conta não encontrada")
        
        amount = Money(command.amount)
        account.deposit(amount, datetime.utcnow())
        self.account_repo.save(account)
        return account
    