import sqlite3
from pathlib import Path
from bank.exceptions import SaldoInsuficienteError, ValorInvalidoError

DB_FILE = Path(__file__).resolve().parent.parent / "bank_system.db"

class Account:
    """
    Representa uma conta bancária com operações de depósito, saque, transferência e extrato.
    """

    def __init__(self, account_id: int, name: str, balance: float = 0.0):
        """
        Inicializa uma nova conta.

        Args:
            account_id (int): ID da conta.
            name (str): Nome do titular da conta.
            balance (float, opcional): Saldo inicial da conta. Padrão é 0.0.
        """
        self.account_id = account_id
        self.name = name
        self.balance = balance

    def _update_balance(self, new_balance: float) -> None:
        """
        Atualiza o saldo da conta no banco de dados.

        Args:
            new_balance (float): Novo saldo a ser atualizado.
        """
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE accounts SET balance = ? WHERE id = ?",
                (new_balance, self.account_id)
            )
            conn.commit()
        self.balance = new_balance

    def _record_transaction(self, type_: str, amount: float) -> None:
        """
        Registra uma transação no banco de dados.

        Args:
            type_ (str): Tipo da transação (ex: 'deposit', 'withdraw', 'transfer_in', 'transfer_out').
            amount (float): Valor da transação.
        """
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)",
                (self.account_id, type_, amount)
            )
            conn.commit()

    def deposit(self, amount: float) -> None:
        """
        Realiza um depósito na conta.

        Args:
            amount (float): Valor a ser depositado.

        Raises:
            ValorInvalidoError: Se o valor do depósito não for positivo.
        """
        if amount <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")

        new_balance = self.balance + amount
        self._update_balance(new_balance)
        self._record_transaction("deposit", amount)
        print(f"Depósito de R$ {amount:.2f} realizado. Saldo atual: R$ {self.balance:.2f}")

    def withdraw(self, amount: float) -> None:
        """
        Realiza um saque da conta.

        Args:
            amount (float): Valor a ser sacado.

        Raises:
            ValorInvalidoError: Se o valor do saque não for positivo.
            SaldoInsuficienteError: Se não houver saldo suficiente.
        """
        if amount <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if amount > self.balance:
            raise SaldoInsuficienteError("Saldo insuficiente para saque.")

        new_balance = self.balance - amount
        self._update_balance(new_balance)
        self._record_transaction("withdraw", amount)
        print(f"Saque de R$ {amount:.2f} realizado. Saldo atual: R$ {self.balance:.2f}")

    def transfer(self, target_id: int, amount: float) -> None:
        """
        Transfere um valor para outra conta.

        Args:
            target_id (int): ID da conta de destino.
            amount (float): Valor a ser transferido.

        Raises:
            ValorInvalidoError: Se o valor da transferência não for positivo.
            SaldoInsuficienteError: Se não houver saldo suficiente.
            ValueError: Se a conta de destino não for encontrada.
        """
        if amount <= 0:
            raise ValorInvalidoError("O valor da transferência deve ser positivo.")
        if amount > self.balance:
            raise SaldoInsuficienteError("Saldo insuficiente para transferência.")

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, balance FROM accounts WHERE id = ?", (target_id,))
            target = cursor.fetchone()
            if not target:
                raise ValueError("Conta destino não encontrada.")

            # Atualiza saldo do remetente
            new_balance = self.balance - amount
            self._update_balance(new_balance)
            self._record_transaction("transfer_out", amount)

            # Atualiza saldo do destinatário
            new_target_balance = target[1] + amount
            cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_target_balance, target_id))
            cursor.execute(
                "INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)",
                (target_id, "transfer_in", amount)
            )
            conn.commit()
        print(f"Transferência de R$ {amount:.2f} realizada para conta {target_id}. Seu saldo atual: R$ {self.balance:.2f}")

    def show_statement(self) -> None:
        """
        Exibe todas as transações da conta, ordenadas por data/hora.
        """
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT type, amount, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp ASC",
                (self.account_id,)
            )
            rows = cursor.fetchall()

        if not rows:
            print("Nenhuma transação encontrada.")
        else:
            for row in rows:
                print(f"[{row[2]}] {row[0]}: R$ {row[1]:.2f}")
            print(f"Saldo atual: R$ {self.balance:.2f}")
