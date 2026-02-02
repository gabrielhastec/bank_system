"""
Caso de Uso: GetStatementUseCase
--------------------------------
Obtém o extrato bancário de uma conta, incluindo transações persistidas.
"""

from datetime import datetime
from typing import List, Dict
from decimal import Decimal

from ..ports.account_repository import IAccountRepository
from ..ports.transaction_repository import ITransactionRepository
from ...domain.value_objects.money import Money

class GetStatementUseCase:
    """Caso de uso para obtenção de extrato bancário."""

    def __init__(
        self, 
        account_repo: IAccountRepository,
        transaction_repo: ITransactionRepository
    ):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def execute(self, account_id: str) -> List[Dict]:
        """
        Obtém o extrato completo de uma conta.
        
        Args:
            account_id: ID da conta
            
        Returns:
            Lista de transações formatadas
            
        Raises:
            ValueError: Se a conta não for encontrada
        """

        # Verifica se a conta existe
        account = self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError("Conta não encontrada")
        
        # Obtém transações do repositório
        transactions = self.transaction_repo.get_by_account_id(account_id)
        
        # Formata transações para resposta
        formatted_transactions = []

        for transaction in transactions:
            formatted_transactions.append({
                "transaction_id": transaction.transaction_id,
                "type": transaction.type,
                "amount": Decimal(str(transaction.amount.amount)),
                "occurred_at": transaction.occurred_at.isoformat(),
                "description": transaction.description
            })

        # Ordena por data (mais recente primeiro)
        formatted_transactions.sort(
            key=lambda x: x["occurred_at"], 
            reverse=True
        )
        return formatted_transactions

    def get_balance(self, account_id: str) -> Dict:
        """
        Obtém o saldo atual de uma conta.
        
        Args:
            account_id: ID da conta
            
        Returns:
            Dicionário com saldo e limites
        """
        
        account = self.account_repo.get_by_id(account_id)
        if not account:
            raise ValueError("Conta não encontrada")
        
        return {
            "account_id": account_id,
            "balance": Decimal(str(account.balance.amount)),
            "daily_withdrawal_limit": Decimal(str(account.daily_withdrawal_limit.amount)),
            "daily_withdrawal_amount": Decimal(str(account.daily_withdrawal_amount.amount)),
            "daily_withdrawal_count": account.daily_withdrawal_count,
            "last_withdrawal_date": account.last_withdrawal_date.isoformat() if account.last_withdrawal_date else None
        }
