from dataclasses import dataclass
from typing import List, Tuple
from bank.models.transaction import Transaction

@dataclass
class Account:
    """
    Representa uma conta bancária com operações de depósito, saque e transferência.
    """
    account_id: int
    name: str
    balance: float = 0.0
    transactions: List[Transaction] = None

    def __post_init__(self):
        if self.transactions is None:
            self.transactions = []

    def deposit(self, amount: float):
        self.balance += amount
        self.transactions.append(Transaction(type="deposit", amount=amount))

    def withdraw(self, amount: float):
        self.balance -= amount
        self.transactions.append(Transaction(type="withdraw", amount=amount))

    def transfer_out(self, amount: float):
        self.balance -= amount
        self.transactions.append(Transaction(type="transfer_out", amount=amount))

    def transfer_in(self, amount: float):
        self.balance += amount
        self.transactions.append(Transaction(type="transfer_in", amount=amount))

    def get_statement(self) -> List[Transaction]:
        return self.transactions
