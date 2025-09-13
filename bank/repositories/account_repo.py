import sqlite3
from pathlib import Path
from bank.models.account import Account
from bank.models.transaction import Transaction

DB_FILE = Path(__file__).resolve().parent.parent / "bank_system.db"

class AccountRepository:
    """Responsável pela persistência das contas no SQLite."""

    @staticmethod
    def create_tables():
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )""")
            conn.commit()

    @staticmethod
    def add_account(account: Account) -> int:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO accounts (name, balance) VALUES (?, ?)",
                (account.name, account.balance)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_account(account_id: int) -> Account:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, balance FROM accounts WHERE id = ?", (account_id,))
            row = cursor.fetchone()
            if not row:
                return None
            cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp ASC", (account_id,))
            transactions = [Transaction(type=t[0], amount=t[1], timestamp=t[2]) for t in cursor.fetchall()]
            return Account(account_id=row[0], name=row[1], balance=row[2], transactions=transactions)

    @staticmethod
    def update_balance(account: Account):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (account.balance, account.account_id))
            conn.commit()

    @staticmethod
    def add_transaction(account_id: int, transaction: Transaction):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)",
                (account_id, transaction.type, transaction.amount)
            )
            conn.commit()
