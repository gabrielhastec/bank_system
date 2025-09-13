from bank.models.account import Account
from bank.repositories.account_repo import AccountRepository
from bank.exceptions import SaldoInsuficienteError, ValorInvalidoError

class AccountService:
    """Camada de lógica de negócios para operações bancárias."""

    @staticmethod
    def deposit(account_id: int, amount: float):
        if amount <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        account = AccountRepository.get_account(account_id)
        account.deposit(amount)
        AccountRepository.update_balance(account)
        AccountRepository.add_transaction(account_id, account.transactions[-1])

    @staticmethod
    def withdraw(account_id: int, amount: float):
        account = AccountRepository.get_account(account_id)
        if amount <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if amount > account.balance:
            raise SaldoInsuficienteError("Saldo insuficiente para saque.")
        account.withdraw(amount)
        AccountRepository.update_balance(account)
        AccountRepository.add_transaction(account_id, account.transactions[-1])

    @staticmethod
    def transfer(from_id: int, to_id: int, amount: float):
        if amount <= 0:
            raise ValorInvalidoError("O valor da transferência deve ser positivo.")
        from_account = AccountRepository.get_account(from_id)
        to_account = AccountRepository.get_account(to_id)
        if amount > from_account.balance:
            raise SaldoInsuficienteError("Saldo insuficiente para transferência.")
        from_account.transfer_out(amount)
        to_account.transfer_in(amount)
        AccountRepository.update_balance(from_account)
        AccountRepository.update_balance(to_account)
        AccountRepository.add_transaction(from_id, from_account.transactions[-1])
        AccountRepository.add_transaction(to_id, to_account.transactions[-1])
