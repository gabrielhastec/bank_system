"""Exceções personalizadas para o domínio bancário.

Este módulo define um conjunto de classes de exceção personalizadas usadas para lidar
com erros específicos do domínio na aplicação bancária, como saldo insuficiente,
contas inválidas, transações inválidas e contas duplicadas. Todas as exceções
herdam da classe base `DomainError`.
"""

class DomainError(Exception):
    """Exceção base para erros de domínio."""
    pass

# Exceções específicas do domínio bancário
class InsufficientFundsError(DomainError):
    """Lançada quando a conta não possui saldo suficiente."""
    def __init__(self, balance: float, attempted: float):
        super().__init__(f"Saldo insuficiente: saldo atual {balance}, tentativa de saque {attempted}.")

class InvalidAccountError(DomainError):
    """Lançada quando uma conta não existe ou está inativa."""
    def __init__(self, account_id: int):
        super().__init__(f"Conta inválida ou inexistente: {account_id}.")

class InvalidTransactionError(DomainError):
    """Lançada quando uma transação é inválida por regra de negócio."""
    def __init__(self, reason: str):
        super().__init__(f"Transação inválida: {reason}.")

class DuplicateAccountError(DomainError):
    """Lançada quando uma conta já existe para o mesmo cliente."""
    def __init__(self, identifier: str):
        super().__init__(f"Já existe uma conta registrada para o identificador '{identifier}'.")

class DailyLimitExceededError(DomainError):
    """Lançada quando a conta atingiu o limite diário de transações."""
    def __init__(self, account_id: int, limit: int, next_allowed_date_iso: str):
        msg = (
            f"Limite diário de {limit} transações atingido para a conta {account_id}. "
            f"Novas transações serão permitidas a partir de {next_allowed_date_iso}."
        )
        super().__init__(msg)
        
class InvalidAmountError(DomainError):
    """Lançada quando um valor monetário é inválido (negativo ou zero)."""
    def __init__(self, amount: float):
        super().__init__(f"Valor inválido: {amount}. Deve ser maior que zero.")

class UserNotFoundError(DomainError):
    """Lançada quando um usuário não é encontrado no sistema."""
    def __init__(self, user_id: int):
        super().__init__(f"Usuário com ID {user_id} não encontrado.")

class UnauthorizedAccessError(DomainError):
    """Lançada quando há uma tentativa de acesso não autorizado a uma conta."""
    def __init__(self, user_id: int, account_id: int):
        super().__init__(f"Usuário {user_id} não autorizado a acessar a conta {account_id}.")

class InvalidCPFError(DomainError):
    """Lançada quando um CPF é inválido."""
    def __init__(self, cpf: str):
        super().__init__(f"CPF inválido: {cpf}.")

class InvalidNameError(DomainError):
    """Lançada quando um nome é inválido."""
    def __init__(self, name: str):
        super().__init__(f"Nome inválido: {name}.")

class InvalidEmailError(DomainError):
    """Lançada quando um endereço de e-mail é inválido."""
    def __init__(self, email: str):
        super().__init__(f"Endereço de e-mail inválido: {email}.")

class InvalidValueError(DomainError):
    """Lançada quando um valor é inválido."""
    def __init__(self, value: str):
        super().__init__(f"Valor inválido: {value}.")
