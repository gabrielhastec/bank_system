"""
Exceções de Domínio
-------------------

Este módulo define todas as exceções específicas da camada de Domínio
da aplicação. Cada exceção representa uma violação de regra de negócio
ou de invariantes do domínio.

As exceções aqui definidas são utilizadas por:
- Entities
- Value Objects
- Aggregates
- Use Cases (apenas para capturar/tratar, nunca para defini-las)

Importante:
Nenhuma exceção aqui depende de detalhes externos (HTTP, banco, libs).
Todo tratamento de conversão (ex.: HTTP 400, 422, etc.) deve ocorrer
na camada de Interface (Delivery Layer).
"""


class DomainException(Exception):
    """
    Exceção base para todas as violações de regras de domínio.

    Todas as exceções específicas herdadas desta classe representam
    erros previstos pelas regras do negócio — e não erros técnicos.
    """
    pass


class InsufficientFunds(DomainException):
    """
    Lançada quando uma operação financeira tenta utilizar
    um valor maior do que o saldo disponível da conta.
    """
    pass


class DailyLimitExceeded(DomainException):
    """
    Lançada quando um cliente ultrapassa algum limite diário,
    seja de valor máximo de saque ou de número máximo de operações.
    """
    pass


class DuplicateCPFException(DomainException):
    """
    Lançada quando a aplicação tenta registrar um CPF que já existe
    no sistema, violando a regra de unicidade do documento.
    """
    pass
