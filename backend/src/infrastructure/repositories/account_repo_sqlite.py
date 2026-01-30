"""
Repositório SQLite: AccountRepositorySQLite
-------------------------------------------

Implementação concreta da porta IAccountRepository localizada na camada
de Infraestrutura da Clean Architecture.

Este repositório é responsável por:
- Persistir aggregates do domínio (Account) no banco SQLite
- Reconstruí-los a partir dos modelos ORM
- Fazer a ponte entre entidades/aggregates e o modelo relacional

Importante:
Este módulo **não contém regras de negócio**.
Ele apenas converte o aggregate Account em um modelo persistível
(AccountModel) e vice-versa.
"""

from select import select
from sqlmodel import Session
from sqlalchemy import exc

from ...application.ports.account_repository import IAccountRepository
from ...domain.aggregates.account import Account
from ..database.models.account_model import AccountModel
from ..database.orm import engine

class AccountRepositorySQLite(IAccountRepository):
    """
    Implementação SQLite da interface IAccountRepository.

    Responsável por persistir e recuperar aggregates Account utilizando
    o modelo de dados definido em AccountModel (SQLModel).
    """

    def save(self, account: Account) -> None:
        """
        Persiste um aggregate Account no banco SQLite.

        Regras aplicadas:
        - Os dados do cliente e do saldo são extraídos do aggregate
        - Converte o aggregate completo para um modelo ORM
        - Trata possíveis erros de integridade, como CPF duplicado

        Raises:
            ValueError: caso o CPF já esteja cadastrado no sistema
        """
        model = AccountModel(
            account_id=account.account_id,
            customer_id=account.customer.customer_id,
            customer_name=account.customer.name,
            customer_email=account.customer.email,
            customer_cpf=str(account.customer.cpf),
            password_hash=(
                account.customer._password.hashed
                if account.customer._password
                else ""
            ),
            balance=account.balance.amount,
        )

        with Session(engine) as session:
            try:
                session.add(model)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
                raise ValueError("CPF já cadastrado no sistema.")

    def get_by_id(self, account_id: str) -> Account | None:
        """
        Recupera um aggregate Account a partir de seu ID, reconstruindo
        a entidade de domínio a partir do modelo persistido.

        Caso o ID não exista, retorna None.

        A reconstrução envolve:
        - Recriar Customer (value objects e senha)
        - Recriar o saldo como Money
        - (TODO) Recarregar lista de transações quando houver tabela própria
        """
        with Session(engine) as session:
            model = session.get(AccountModel, account_id)
            if not model:
                return None

            # Importações locais para evitar acoplamento circular
            from ...domain.entities.customer import Customer
            from ...domain.value_objects.cpf import CPF
            from ...domain.value_objects.password import Password
            from ...domain.value_objects.money import Money

            # Reconstrói o Customer
            password = (
                Password(hashed=model.password_hash)
                if model.password_hash
                else None
            )

            customer = Customer(
                name=model.customer_name,
                email=model.customer_email,
                cpf=CPF(model.customer_cpf),
                customer_id=model.customer_id,
                _password=password
            )

            # Reconstrói o Account aggregate
            account = Account(
                account_id=model.account_id,
                customer=customer,
                balance=Money(str(model.balance)),
                transactions=[]  # TODO: Carregar transações quando modelo existir
            )

            return account

    def get_by_cpf(self, cpf: str) -> Account | None:
        with Session(engine) as session:
            stmt = select(AccountModel).where(
                AccountModel.customer_cpf == cpf
            )
            model = session.exec(stmt).first()
            if not model:
                return None
            # Reconstruir a conta (igual no get_by_id)
            from ...domain.entities.customer import Customer
            from ...domain.value_objects.cpf import CPF
            from ...domain.value_objects.password import Password
            from ...domain.value_objects.money import Money

            password = (
                Password(hashed=model.password_hash)
                if model.password_hash
                else None
            )

            customer = Customer(
                name=model.customer_name,
                email=model.customer_email,
                cpf=CPF(model.customer_cpf),
                customer_id=model.customer_id,
                _password=password
            )

            account = Account(
                account_id=model.account_id,
                customer=customer,
                balance=Money(str(model.balance)),
                transactions=[]  # TODO: Carregar transações
            )

            return account
