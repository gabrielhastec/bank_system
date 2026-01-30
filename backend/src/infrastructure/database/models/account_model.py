"""
Modelo ORM: AccountModel
------------------------
Representa a tabela de contas no banco SQLite utilizando SQLModel.

Este modelo pertence à camada de infraestrutura e tem como objetivo
mapear os dados persistidos no banco para estruturas Python que podem
ser convertidas para entidades de domínio quando necessário.

Importante:
- O domínio não conhece este modelo
- Apenas repositórios da infraestrutura interagem diretamente com ele
- Campos relacionados ao cliente estão “embutidos” (denormalização leve)
"""

from sqlmodel import SQLModel, Field
from decimal import Decimal
from datetime import date
from typing import Optional


class AccountModel(SQLModel, table=True):
    """
    Modelo ORM para persistência de contas bancárias.

    Campos:
    - account_id: identificador único da conta
    - customer_id: identificador do cliente (ainda não usado totalmente)
    - customer_name: nome do titular
    - customer_email: email do titular
    - customer_cpf: CPF do titular (único no sistema)
    - customer_birth_date: data de nascimento, opcional
    - password_hash: hash da senha do cliente
    - balance: saldo da conta com precisão decimal
    """

    account_id: str = Field(primary_key=True)
    customer_id: str = Field(index=True)  # Adicionado
    customer_name: str = Field(index=True)
    customer_email: str = Field(index=True)  # Adicionado
    customer_cpf: str = Field(index=True, unique=True)
    customer_birth_date: Optional[date] = None
    password_hash: str
    balance: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=12)
