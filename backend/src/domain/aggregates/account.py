"""
Aggregate de domínio: Account
-----------------------------

Representa a entidade raiz (aggregate root) responsável por modelar
uma conta bancária dentro da camada de Domínio da Clean Architecture.

Este aggregate encapsula:
- Estado e regras de negócio relacionadas ao saldo, transações e limites
- Invariantes de domínio (ex.: limite diário de saque, contagem de saques)
- Comportamentos essenciais: abrir conta, depósito, saque, extrato

Importante:
Este arquivo contém exclusivamente *lógica de domínio*, sem dependências
de frameworks, transporte HTTP ou banco de dados.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List

from ..entities.customer import Customer
from ..value_objects.money import Money
from ...domain.exceptions import InsufficientFunds, DailyLimitExceeded

@dataclass
class Account:
    """
    Aggregate root que representa uma conta bancária no domínio.

    Responsável por:
    - Armazenar informações principais (cliente, saldo, transações)
    - Garantir regras de negócio e invariantes de domínio
    - Coordenar operações de depósito, saque e abertura da conta
    """

    account_id: str
    customer: Customer
    balance: Money = field(default_factory=lambda: Money("0.00"))
    transactions: List[dict] = field(default_factory=list)

    # Regras de limite diário
    daily_withdrawal_limit: Money = Money("3000.00")
    daily_withdrawal_amount: Money = field(default_factory=lambda: Money("0.00"))
    daily_withdrawal_count: int = 0
    last_withdrawal_date: date | None = None

    @classmethod
    def open(cls, customer: Customer) -> "Account":
        """
        Factory method responsável pela criação de uma nova conta.

        Esta operação pertence ao domínio pois envolve regras e valores
        iniciais da aggregate root.
        """
        import uuid

        return cls(
            account_id=str(uuid.uuid4()),
            customer=customer,
            balance=Money("0.00"),
            transactions=[]
        )

    def deposit(self, amount: Money, occurred_at: datetime):
        """
        Realiza um depósito na conta.

        Regras aplicadas:
        - Somar o valor ao saldo
        - Registrar a transação no histórico
        """
        self.balance += amount

        self.transactions.append({
            "type": "deposit",
            "amount": amount,
            "occurred_at": occurred_at.isoformat()
        })

    def withdraw(self, amount: Money, occurred_at: datetime):
        """
        Realiza um saque aplicando todas as regras de negócio:

        Regras aplicadas:
        - Reset diário caso haja mudança de data
        - Verificar saldo suficiente
        - Verificar limite de saque diário em valor
        - Verificar limite de quantidade de saques por dia
        - Atualizar saldo, limites e registrar transação
        """
        today = occurred_at.date()

        # Reset diário dos limites
        if self.last_withdrawal_date != today:
            self.daily_withdrawal_amount = Money("0.00")
            self.daily_withdrawal_count = 0
            self.last_withdrawal_date = today

        # Regras de domínio
        if self.balance < amount:
            raise InsufficientFunds("Saldo insuficiente")

        if self.daily_withdrawal_amount + amount > self.daily_withdrawal_limit:
            raise DailyLimitExceeded(
                "Limite diário de saque excedido (R$ 3.000)"
            )

        if self.daily_withdrawal_count >= 5:
            raise DailyLimitExceeded(
                "Limite de 5 saques por dia excedido"
            )

        # Aplicação das mudanças de estado
        self.balance -= amount
        self.daily_withdrawal_amount += amount
        self.daily_withdrawal_count += 1

        self.transactions.append({
            "type": "withdrawal",
            "amount": amount,
            "occurred_at": occurred_at.isoformat()
        })

    def get_statement(self) -> List[dict]:
        """
        Retorna uma cópia imutável da lista de transações da conta
        (evita mutação externa do estado interno do aggregate).
        """
        return self.transactions.copy()
