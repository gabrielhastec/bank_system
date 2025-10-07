"""Módulo de domínio para a aplicação bancária.

Este módulo agrupa funcionalidades e definições relacionadas à lógica de negócio
do sistema bancário, incluindo exceções personalizadas para tratamento de erros
específicos do domínio.
"""

from .exceptions import (
    DomainError,
    InsufficientFundsError,
    InvalidAccountError,
    InvalidTransactionError,
    DuplicateAccountError,
)

__all__ = [
    "DomainError",
    "InsufficientFundsError",
    "InvalidAccountError",
    "InvalidTransactionError",
    "DuplicateAccountError",
]
