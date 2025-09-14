import pytest
from bank.models.account import Account
from bank.exceptions import SaldoInsuficienteError, ValorInvalidoError, LimiteSaquesExcedidoError

def test_depositar_aumenta_saldo():
    """
    Testa se o saldo aumenta corretamente após um depósito.
    """
    conta = Account("Gabriel", balance=1050.0)
    conta.depositar(200)
    assert conta.balance == 1250.0
    assert conta.transactions[-1].tipo == "deposito"

def test_sacar_diminui_saldo():
    """
    Testa se o saldo diminui corretamente após um saque.
    """
    conta = Account("Gabriel", balance=1050.0)
    conta.depositar(200)
    conta.sacar(100)
    assert conta.balance == 1150.0
    assert conta.transactions[-1].tipo == "saque"

def test_saque_maior_que_saldo():
    """
    Testa se uma exceção é lançada ao tentar sacar valor maior que o saldo.
    """
    conta = Account("Gabriel", balance=50.0)
    with pytest.raises(SaldoInsuficienteError):
        conta.sacar(100)

def test_extrato_retorna_transacoes():
    """
    Testa se o extrato retorna corretamente as transações realizadas.
    """
    conta = Account("Gabriel", balance=1050.0)
    conta.depositar(100)
    conta.sacar(30)
    transacoes, saldo = conta.extrato()
    assert len(transacoes) == 2
    assert transacoes[0].tipo == "deposito"
    assert transacoes[1].tipo == "saque"

def test_deposito_valor_invalido():
    """
    Testa se uma exceção é lançada ao tentar depositar valor zero ou negativo.
    """
    conta = Account("Gabriel", balance=100.0)
    with pytest.raises(ValorInvalidoError):
        conta.depositar(0)
    with pytest.raises(ValorInvalidoError):
        conta.depositar(-50)

def test_saque_valor_invalido():
    """
    Testa se uma exceção é lançada ao tentar sacar valor zero ou negativo.
    """
    conta = Account("Gabriel", balance=100.0)
    with pytest.raises(ValorInvalidoError):
        conta.sacar(0)
    with pytest.raises(ValorInvalidoError):
        conta.sacar(-10)

def test_limite_saques_excedido():
    """
    Testa se uma exceção é lançada ao exceder o número máximo de saques permitidos.
    """
    conta = Account("Gabriel", balance=1000.0, max_saques=2)
    conta.sacar(100)
    conta.sacar(100)
    with pytest.raises(LimiteSaquesExcedidoError):
        conta.sacar(100)

def test_saque_excede_limite():
    """
    Testa se uma exceção é lançada ao tentar sacar valor acima do limite permitido por saque.
    """
    conta = Account("Gabriel", balance=1000.0, saque_limite=300.0)
    with pytest.raises(ValorInvalidoError):
        conta.sacar(400)