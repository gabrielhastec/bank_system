"""
Exemplo de uso do sistema bancário.

Este módulo permite criar contas, realizar login e executar operações bancárias
como depósito, saque, transferência e consulta de extrato.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
from pathlib import Path
from bank.account import Account

DB_FILE = Path(__file__).resolve().parent.parent / "bank_system.db"

def init_db():
    """
    Inicializa o banco de dados, criando as tabelas necessárias se não existirem.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        """)
        conn.commit()

def create_account():
    """
    Cria uma nova conta bancária solicitando o nome do titular ao usuário.
    """
    name = input("Digite o nome do titular: ").strip()
    if not name:
        print("Nome não pode ser vazio.")
        return
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, 0.0))
        conn.commit()
        print(f"Conta criada com sucesso! ID: {cursor.lastrowid}")

def login():
    """
    Realiza o login do usuário solicitando o ID da conta.

    Returns:
        Account: Instância da conta logada, ou None se não encontrada.
    """
    try:
        account_id = int(input("Digite o ID da sua conta: "))
    except ValueError:
        print("ID inválido. Digite um número inteiro.")
        return None
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
    if row:
        print(f"Bem-vindo(a), {row[1]}! Saldo atual: R$ {row[2]:.2f}")
        return Account(account_id=row[0], name=row[1], balance=row[2])
    print("Conta não encontrada.")
    return None

def main_menu(account: Account):
    """
    Exibe o menu principal para operações bancárias.

    Args:
        account (Account): Conta do usuário logado.
    """
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Extrato")
        print("4. Transferir")
        print("5. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                valor = float(input("Digite o valor para depósito: "))
                account.deposit(valor)
            except ValueError:
                print("Valor inválido.")
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "2":
            try:
                valor = float(input("Digite o valor para saque: "))
                account.withdraw(valor)
            except ValueError:
                print("Valor inválido.")
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "3":
            print("\n--- Extrato ---")
            account.show_statement()
        elif opcao == "4":
            try:
                destino_id = int(input("Digite o ID da conta destino: "))
                valor = float(input("Digite o valor da transferência: "))
                account.transfer(destino_id, valor)
            except ValueError:
                print("ID ou valor inválido.")
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def run_example():
    """
    Executa o exemplo interativo do sistema bancário.
    """
    init_db()
    while True:
        print("\n=== SISTEMA BANCÁRIO ===")
        print("1. Criar conta")
        print("2. Login")
        print("3. Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            acc = login()
            if acc:
                main_menu(acc)
        elif choice == "3":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    run_example()
