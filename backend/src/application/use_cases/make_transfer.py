
from dataclasses import dataclass
from datetime import datetime

from ...domain.aggregates.account import Account
from ..ports.account_repository import IAccountRepository
from ...domain.value_objects.money import Money

@dataclass
class TransferCommand:
    source_account_id: str
    target_account_id: str
    amount: str

class MakeTransferUseCase:
    def __init__(self, account_repo: IAccountRepository):
        self.account_repo = account_repo

    def execute(self, command: TransferCommand):
        source = self.account_repo.get_by_id(command.source_account_id)
        target = self.account_repo.get_by_id(command.target_account_id)
        
        if not source or not target:
            raise ValueError("Conta de origem ou destino não encontrada")
        
        amount = Money(command.amount)
        
        # Realizar a transferência: debitar da origem e creditar no destino
        source.withdraw(amount, datetime.utcnow())
        target.deposit(amount, datetime.utcnow())
        
        self.account_repo.save(source)
        self.account_repo.save(target)
        
        return source
