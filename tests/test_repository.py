from bank.repositories.account_repo import AccountRepository

"""
Módulo de testes para o repositório de contas do sistema bancário.

Contém testes para validar a criação e recuperação de contas no banco de dados
usando o AccountRepository.
"""

def test_create_and_get() -> None:
    """Testa a criação de uma conta e sua recuperação pelo ID.

    Cria uma conta com CPF, nome e saldo inicial, recupera-a pelo ID e valida
    que o CPF e o saldo correspondem aos valores fornecidos.
    """
    repo = AccountRepository()
    acc = repo.create_account("98765432100", "Tester", balance=10.0)
    got = repo.get_account_by_id(acc.id)
    assert got.cpf == "98765432100"
    assert got.balance == 10.0
