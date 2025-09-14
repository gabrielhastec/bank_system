"""Módulo de exceções personalizadas para gerenciamento de contas.

Define exceções específicas para erros relacionados a valores inválidos, saldo insuficiente,
contas não encontradas e tentativas de criar contas duplicadas.
"""

class ValorInvalidoError(Exception):
    """Exceção lançada quando um valor fornecido é inválido.

    Um valor é considerado inválido se for negativo, zero ou de um tipo incorreto
    (por exemplo, uma string em vez de um número).
    """
    pass

class SaldoInsuficienteError(Exception):
    """Exceção lançada quando o saldo de uma conta é insuficiente para uma operação.

    Isso ocorre em tentativas de saques ou transferências que excedem o saldo disponível.
    """
    pass

class ContaNaoEncontradaError(Exception):
    """Exceção lançada quando uma conta não é encontrada no repositório.

    Isso ocorre ao tentar acessar ou operar em uma conta com identificador inexistente.
    """
    pass

class ContaDuplicadaError(Exception):
    """Exceção lançada ao tentar criar uma conta duplicada.

    Isso ocorre quando já existe uma conta com o mesmo CPF ou identificador no repositório.
    """
    pass