from dataclasses import dataclass, field
from typing import List
from bank.infrastructure.utils.validators import validate_cpf, validate_name, ensure_positive_number
from bank.domain.exceptions import (
    ValorInvalidoError,
    SaldoInsuficienteError
)
from bank.domain.entities.transaction import Transaction

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

    def __post_init__(self):
        """Valida os atributos após a inicialização do objeto.

        Raises:
            ValorInvalidoError: Se o saldo inicial for negativo.
        """
        validate_cpf(self.cpf)   # Ex.: Checa formato "12345678901"
        validate_name(self.name)    # Ex.: Garante que não é vazio
        if self.balance < 0:
            raise ValorInvalidoError("Saldo inicial não pode ser negativo.")

    def deposit_local(self, amount: float) -> None:
        """Realiza um depósito no saldo da conta, atualizando o objeto em memória.

        Args:
            amount (float): Valor a ser depositado.

        Note:
            Esta operação não persiste os dados em um banco de dados.
            Uma transação do tipo 'deposit' é adicionada ao histórico.
        """
        amount = ensure_positive_number(amount)
        self.balance += amount

    def withdraw_local(self, amount: float) -> None:
        """Realiza um saque do saldo da conta, atualizando o objeto em memória.

        Args:
            amount (float): Valor a ser sacado.

        Note:
            Esta operação não persiste os dados em um banco de dados.
            Uma transação do tipo 'withdraw' é adicionada ao histórico.
        """
        amount = ensure_positive_number(amount)
        if amount > self.balance:
            raise SaldoInsuficienteError("Saldo insuficiente para saque.")
        self.balance -= amount

    def as_dict(self) -> dict:
        """Serializa a conta em um dicionário, incluindo transações.
        Returns:
            dict: Representação em dicionário da conta e suas transações.
        """
        return {
            "id": self.id,
            "cpf": self.cpf,
            "name": self.name,
            "balance": self.balance,
            "transactions": [t.as_dict() for t in self.transactions]
        }
