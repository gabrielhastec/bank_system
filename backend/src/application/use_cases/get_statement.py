
from ..ports.account_repository import IAccountRepository

class GetStatementUseCase:
    def __init__(self, account_repo: IAccountRepository):
        self.account_repo = account_repo

    def execute(self, account_id: str):
        account = self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError("Conta não encontrada")
        
        return account.get_statement()
