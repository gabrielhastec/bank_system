from dataclasses import dataclass, field
from typing import List
from .transaction import Transaction

"""Módulo que define a classe Account para gerenciamento de contas financeiras.

A classe Account representa uma conta com atributos como identificador, CPF, nome, saldo
e histórico de transações, além de métodos para depósitos, saques e serialização.
"""

@dataclass
class Account:
    """Classe que representa uma conta financeira.

    Atributos:
        id (int): Identificador único da conta.
        cpf (str): CPF do titular da conta.
        name (str): Nome do titular da conta.
        balance (float): Saldo atual da conta, inicializado como 0.0.
        transactions (List[Transaction]): Lista de transações associadas à conta.
    """
    id: int
    cpf: str
    name: str
    balance: float = 0.0
    transactions: List[Transaction] = field(default_factory=list)

    def deposit_local(self, amount: float) -> None:
        """Realiza um depósito no saldo da conta, atualizando o objeto em memória.

        Args:
            amount (float): Valor a ser depositado.

        Note:
            Esta operação não persiste os dados em um banco de dados.
            Uma transação do tipo 'deposit' é adicionada ao histórico.
        """
        self.balance += amount
        self.transactions.append(Transaction(id=None, account_id=self.id, type="deposit", amount=amount, timestamp=None))

    def withdraw_local(self, amount: float) -> None:
        """Realiza um saque do saldo da conta, atualizando o objeto em memória.

        Args:
            amount (float): Valor a ser sacado.

        Note:
            Esta operação não persiste os dados em um banco de dados.
            Uma transação do tipo 'withdraw' é adicionada ao histórico.
        """
        self.balance -= amount
        self.transactions.append(Transaction(id=None, account_id=self.id, type="withdraw", amount=amount, timestamp=None))

    def as_dict(self) -> dict:
        """Retorna uma representação da conta como dicionário.

        Returns:
            dict: Dicionário contendo os atributos id, cpf, name e balance.
        """
        return {"id": self.id, "cpf": self.cpf, "name": self.name, "balance": self.balance}