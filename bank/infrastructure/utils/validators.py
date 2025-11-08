"""Módulo de validações básicas de entrada de dados.

Fornece funções para validar formatos de CPF, nomes e valores numéricos positivos,
lançando exceções personalizadas quando as validações falham.
"""

import re
from bank.domain.exceptions import (
    DomainError,
    InvalidAmountError,
    InvalidNameError,
    InvalidCPFError,
    InvalidEmailError,
    InvalidValueError
)

def validate_cpf(cpf: str) -> None:
    """Valida o formato básico de um CPF.

    Verifica se o CPF contém exatamente 11 dígitos numéricos.

    Args:
        cpf (str): CPF a ser validado.

    Raises:
        ValorInvalidoError: Se o CPF não contiver 11 dígitos numéricos.
    """
    if not re.fullmatch(r"\d{11}", cpf):
        raise InvalidCPFError("CPF inválido. Deve conter 11 dígitos numéricos.")

def validate_name(name: str) -> None:
    """Valida o formato de um nome.

    Verifica se o nome não está vazio e contém apenas letras e espaços.

    Args:
        name (str): Nome a ser validado.

    Raises:
        ValorInvalidoError: Se o nome estiver vazio ou contiver caracteres inválidos.
    """
    if not name or not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", name):
        raise InvalidNameError(name)

def ensure_positive_number(value: float) -> float:
    """Garante que o valor é um número positivo.

    Converte o valor para float e verifica se é maior que zero.

    Args:
        value: Valor a ser validado (pode ser float, int ou str convertível).

    Returns:
        float: O valor convertido para float, se válido.

    Raises:
        ValorInvalidoError: Se o valor não for um número ou for menor ou igual a zero.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise InvalidValueError(value)

    # Verifica se o valor é maior que zero
    if value <= 0:
        raise InvalidValueError(value)

    # Verifica se o valor é um número
    if not isinstance(value, float):
        raise InvalidValueError(value)

    # Verifica se o valor é maior que zero
    if value <= 0:
        raise InvalidValueError(value)
    return value
