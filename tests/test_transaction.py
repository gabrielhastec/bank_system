import pytest
from bank.transaction import Transaction

def test_criar_transacao_deposito():
    """
    Testa a criação de uma transação do tipo depósito.
    """
    t = Transaction("deposito", 100.0)
    assert t.tipo == "deposito"
    assert t.valor == 100.0
    assert isinstance(t.to_dict(), dict)

def test_repr_transacao():
    """
    Testa a representação textual (__repr__) de uma transação.
    """
    t = Transaction("saque", 50.0)
    assert "<Transaction tipo=saque valor=50.00>" in repr(t)

def test_to_dict_transacao():
    """
    Testa se o método to_dict retorna um dicionário correto da transação.
    """
    t = Transaction("deposito", 200.0)
    d = t.to_dict()
    assert d == {"tipo": "deposito", "valor": 200.0}