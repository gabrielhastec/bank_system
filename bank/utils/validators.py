from typing import Any

"""Módulo para validação de entradas em um sistema financeiro.

Fornece funções para garantir que valores sejam números positivos e que CPFs
estejam em um formato válido.
"""

def ensure_positive_number(value: Any) -> float:
    """Converte e valida que o valor fornecido é um número positivo.

    Args:
        value (Any): Valor a ser validado e convertido para float.

    Returns:
        float: Valor convertido para float, se válido.

    Raises:
        ValueError: Se o valor não for numérico ou não for positivo.
    """
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError("Valor deve ser numérico.")
    if v <= 0:
        raise ValueError("Valor deve ser positivo.")
    return v

def ensure_cpf_format(cpf: str) -> str:
    """Valida e formata um CPF, retornando apenas os dígitos.

    Remove espaços e caracteres não numéricos do CPF e verifica se o resultado
    contém pelo menos 8 dígitos.

    Args:
        cpf (str): CPF a ser validado.

    Returns:
        str: CPF formatado, contendo apenas dígitos.

    Raises:
        ValueError: Se o CPF estiver vazio ou tiver menos de 8 dígitos após formatação.
    """
    cpf = str(cpf).strip()
    if not cpf:
        raise ValueError("CPF vazio.")
    # Validação simples: apenas dígitos (pode ser ampliada)
    digits = "".join(ch for ch in cpf if ch.isdigit())
    if len(digits) < 8:
        raise ValueError("CPF inválido (muito curto).")
    return digits
