"""
Repositório SQLite: TransactionRepositorySQLite
------------------------------------------------
Implementação concreta da porta ITransactionRepository.
"""

from sqlmodel import Session, select
from typing import List

from ...application.ports.transaction_repository import ITransactionRepository
from ...domain.entities.transaction import Transaction
from ...domain.value_objects.money import Money
from ..database.orm import engine
from ..database.models.transaction_model import TransactionModel

class TransactionRepositorySQLite(ITransactionRepository):
    """
    Implementação SQLite da interface ITransactionRepository.
    """

    def save(self, transaction: Transaction) -> None:
        """
        Persiste uma transação no banco SQLite.
        """

        model = TransactionModel(
            transaction_id=transaction.transaction_id,
            account_id=transaction.account_id,
            type=transaction.type,
            amount=transaction.amount.amount,
            occurred_at=transaction.occurred_at,
            description=transaction.description,
            target_account_id=getattr(transaction, 'target_account_id', None)
        )

        with Session(engine) as session:
            session.add(model)
            session.commit()

    def get_by_account_id(self, account_id: str) -> list[Transaction]:
        """
        Recupera todas as transações de uma conta.
        """

        with Session(engine) as session:
            stmt = select(TransactionModel).where(
                TransactionModel.account_id == account_id
            ).order_by(TransactionModel.occurred_at.desc())

            results = session.exec(stmt).all()

            transactions = []
            for model in results:
                transaction = Transaction(
                    transaction_id=model.transaction_id,
                    account_id=model.account_id,
                    type=model.type,
                    amount=Money(str(model.amount)),
                    occurred_at=model.occurred_at,
                    description=model.description
                )
                transactions.append(transaction)
            
            return transactions
        
    def get_by_id(self, transaction_id: str) -> Transaction | None:
        """
        Busca uma transação pelo ID.
        
        Args:
            transaction_id: ID da transação
            
        Returns:
            Transação encontrada ou None
        """
        with Session(engine) as session:
            model = session.get(TransactionModel, transaction_id)
            if not model:
                return None
            
            return Transaction(
                transaction_id=model.transaction_id,
                account_id=model.account_id,
                type=model.type,
                amount=Money(str(model.amount)),
                occurred_at=model.occurred_at,
                description=model.description
            )
    
    def get_recent_transactions(self, account_id: str, limit: int = 10) -> List[Transaction]:
        """
        Obtém as transações mais recentes de uma conta.
        
        Args:
            account_id: ID da conta
            limit: Número máximo de transações
            
        Returns:
            Lista de transações recentes
        """
        with Session(engine) as session:
            stmt = select(TransactionModel).where(
                TransactionModel.account_id == account_id
            ).order_by(
                TransactionModel.occurred_at.desc()
            ).limit(limit)

            results = session.exec(stmt).all()

            transactions = []
            for model in results:
                transaction = Transaction(
                    transaction_id=model.transaction_id,
                    account_id=model.account_id,
                    type=model.type,
                    amount=Money(str(model.amount)),
                    occurred_at=model.occurred_at,
                    description=model.description
                )
                transactions.append(transaction)
            
            return transactions
