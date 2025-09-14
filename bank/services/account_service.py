from bank.repositories.account_repo import AccountRepository
from bank.exceptions import ValorInvalidoError, SaldoInsuficienteError, ContaNaoEncontradaError
from bank.utils.validators import ensure_positive_number
from bank.core.db import get_connection

"""Módulo que define a classe AccountService para regras de negócio de contas.

Fornece métodos para criação de contas, depósitos, saques, transferências e consulta
de extratos, utilizando o repositório de contas para persistência.
"""

class AccountService:
    """Classe para gerenciar regras de negócio de contas e transações.

    Utiliza um AccountRepository para interagir com o banco de dados e aplicar
    validações e operações financeiras, como depósitos, saques e transferências.
    """

    def __init__(self) -> None:
        """Inicializa o serviço com um repositório de contas."""
        self.repo = AccountRepository()

    def create_account(self, cpf: str, name: str, balance: float = 0.0) -> 'Account':
        """Cria uma nova conta com os dados fornecidos.

        Args:
            cpf (str): CPF do titular da conta.
            name (str): Nome do titular da conta.
            balance (float): Saldo inicial da conta (padrão 0.0).

        Returns:
            Account: Objeto Account representando a conta criada.
        """
        return self.repo.create_account(cpf=cpf, name=name, balance=balance)

    def deposit(self, account_id: int, amount: float) -> None:
        """Realiza um depósito em uma conta e registra a transação.

        Args:
            account_id (int): Identificador único da conta.
            amount (float): Valor a ser depositado.

        Raises:
            ValorInvalidoError: Se o valor não for um número positivo.
            ContaNaoEncontradaError: Se a conta não for encontrada.
        """
        amount = ensure_positive_number(amount)
        account = self.repo.get_account_by_id(account_id)
        account.deposit_local(amount)
        self.repo.update_balance(account_id, account.balance)
        self.repo.add_transaction(account_id, "deposit", amount)

    def withdraw(self, account_id: int, amount: float) -> None:
        """Realiza um saque de uma conta e registra a transação.

        Args:
            account_id (int): Identificador único da conta.
            amount (float): Valor a ser sacado.

        Raises:
            ValorInvalidoError: Se o valor não for um número positivo.
            ContaNaoEncontradaError: Se a conta não for encontrada.
            SaldoInsuficienteError: Se o saldo for insuficiente para o saque.
        """
        amount = ensure_positive_number(amount)
        account = self.repo.get_account_by_id(account_id)
        if amount > account.balance:
            raise SaldoInsuficienteError("Saldo insuficiente.")
        account.withdraw_local(amount)
        self.repo.update_balance(account_id, account.balance)
        self.repo.add_transaction(account_id, "withdraw", amount)

    def transfer(self, source_id: int, target_id: int, amount: float) -> None:
        """Realiza uma transferência entre duas contas, registrando as transações.

        Args:
            source_id (int): Identificador da conta de origem.
            target_id (int): Identificador da conta de destino.
            amount (float): Valor a ser transferido.

        Raises:
            ValorInvalidoError: Se o valor não for um número positivo.
            ContaNaoEncontradaError: Se a conta de origem ou destino não for encontrada.
            SaldoInsuficienteError: Se o saldo da conta de origem for insuficiente.
        """
        amount = ensure_positive_number(amount)
        with get_connection() as conn:
            cur = conn.cursor()
            # Obter saldos
            cur.execute("SELECT id, balance FROM accounts WHERE id = ?", (source_id,))
            src = cur.fetchone()
            cur.execute("SELECT id, balance FROM accounts WHERE id = ?", (target_id,))
            tgt = cur.fetchone()
            if not src:
                raise ContaNaoEncontradaError(f"Conta origem {source_id} não encontrada.")
            if not tgt:
                raise ContaNaoEncontradaError(f"Conta destino {target_id} não encontrada.")
            if amount > src["balance"]:
                raise SaldoInsuficienteError("Saldo insuficiente para transferência.")
            # Atualizar saldos
            new_src = src["balance"] - amount
            new_tgt = tgt["balance"] + amount
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_src, source_id))
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_tgt, target_id))
            # Registrar transações
            cur.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (source_id, "transfer_out", amount))
            cur.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (target_id, "transfer_in", amount))
            conn.commit()

    def get_statement(self, account_id: int) -> List['Transaction']:
        """Recupera o extrato de transações de uma conta.

        Args:
            account_id (int): Identificador único da conta.

        Returns:
            List[Transaction]: Lista de transações associadas à conta.
        """
        return self.repo.list_transactions(account_id)