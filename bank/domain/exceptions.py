"""Exceções personalizadas para o domínio bancário.

Este módulo define um conjunto de classes de exceção personalizadas usadas para lidar
com erros específicos do domínio na aplicação bancária, como saldo insuficiente,
contas inválidas, transações inválidas e contas duplicadas. Todas as exceções
herdam da classe base `DomainError`.
"""

class DomainError(Exception):
    """Exceção base para erros de domínio."""
    pass

class InsufficientFundsError(DomainError):
    """Lançada quando a conta não possui saldo suficiente."""
    def __init__(self, balance: float, attempted: float):
        super().__init__(f"Saldo insuficiente: saldo atual {balance}, tentativa de saque {attempted}.")

class InvalidAccountError(DomainError):
    """Lançada quando uma conta não existe ou está inativa."""
    def __init__(self, account_id: str):
        super().__init__(f"Conta inválida ou inexistente: {account_id}.")

class InvalidTransactionError(DomainError):
    """Lançada quando uma transação é inválida por regra de negócio."""
    def __init__(self, reason: str):
        super().__init__(f"Transação inválida: {reason}.")

class DuplicateAccountError(DomainError):
    """Lançada quando uma conta já existe para o mesmo cliente."""
    def __init__(self, identifier: str):
        super().__init__(f"Já existe uma conta registrada para o identificador '{identifier}'.")
