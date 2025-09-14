import pytest
from bank.services.account_service import AccountService
from bank.exceptions import SaldoInsuficienteError, ValorInvalidoError

"""
Módulo de testes para o serviço de contas do sistema bancário.

Contém testes para validar operações de depósito, saque e transferência,
garantindo o comportamento correto do AccountService.
"""

def test_deposit_and_withdraw() -> None:
    """Testa depósito e saque em uma conta, verificando o saldo final.

    Cria uma conta, realiza um depósito de 200 e um saque de 50, e valida
    que o saldo final é 150.
    """
    svc = AccountService()
    acc = svc.create_account(cpf="12345678900", name="Gabriel")
    svc.deposit(acc.id, 200)
    svc.withdraw(acc.id, 50)
    # Recarrega e valida balance
    acc2 = svc.repo.get_account_by_id(acc.id)
    assert acc2.balance == pytest.approx(150.0)

def test_transfer_insufficient() -> None:
    """Testa transferência com saldo insuficiente, esperando exceção.

    Cria duas contas e tenta transferir 100 da primeira para a segunda,
    que não tem saldo suficiente, verificando se SaldoInsuficienteError é lançada.
    """
    svc = AccountService()
    a1 = svc.create_account(cpf="11111111111", name="A")
    a2 = svc.create_account(cpf="22222222222", name="B")
    with pytest.raises(SaldoInsuficienteError):
        svc.transfer(a1.id, a2.id, 100)
