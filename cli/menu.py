from bank.domain.usecases.make_deposit import MakeDepositUseCase
from bank.domain.usecases.make_withdrawal import MakeWithdrawalUseCase
from bank.domain.usecases.make_transfer import MakeTransferUseCase
from bank.domain.usecases.open_account import OpenAccountUseCase
from bank.infrastructure.persistence.repositories.account_repo_sqlite import AccountRepositorySQLite
from bank.infrastructure.persistence.repositories.transaction_repo_sqlite import TransactionRepositorySQLite
from bank.infrastructure.persistence.repositories.user_repo_sqlite import UserRepositorySQLite
from bank.core.database.connection import get_db_connection

class BankMenu:
    def __init__(self):
        # Inicializa conexão e repositórios
        self.conn = get_db_connection()
        self.account_repo = AccountRepositorySQLite(self.conn)
        self.transaction_repo = TransactionRepositorySQLite(self.conn)
        self.user_repo = UserRepositorySQLite(self.conn)
        
        # Inicializa casos de uso
        self.open_account_use_case = OpenAccountUseCase(self.account_repo, self.user_repo)
        self.deposit_use_case = MakeDepositUseCase(self.account_repo, self.transaction_repo)
        self.withdraw_use_case = MakeWithdrawalUseCase(self.account_repo, self.transaction_repo)
        self.transfer_use_case = MakeTransferUseCase(self.account_repo, self.transaction_repo)

    # Método para exibir o menu e processar entradas do usuário
    def run(self):
        return self.display_menu()

    # Exibe o menu e processa as opções do usuário
    def display_menu(self):
        while True:
            print("\n=== Sistema Bancário ===")
            print("1. Abrir Nova Conta")
            print("2. Fazer Depósito")
            print("3. Fazer Saque")
            print("4. Fazer Transferência")
            print("5. Consultar Saldo")
            print("0. Sair")
            
            # Processa a escolha do usuário
            try:
                option = input("\nEscolha uma opção: ")
                if option == "1":
                    self.handle_open_account()
                elif option == "2":
                    self.handle_deposit()
                elif option == "3":
                    self.handle_withdrawal()
                elif option == "4":
                    self.handle_transfer()
                elif option == "5":
                    self.handle_balance()
                elif option == "0":
                    print("Obrigado por usar nosso sistema!")
                    break
                else:
                    print("Opção inválida!")
            except Exception as e:
                print(f"Erro: {str(e)}")

    # Manipuladores para cada opção do menu
    def handle_open_account(self):
        user_id = int(input("ID do usuário: "))
        try:
            account = self.open_account_use_case.execute(user_id)
            print(f"Conta criada com sucesso! Número da conta: {getattr(account, 'id', account)}")
        except Exception as e:
            print(f"Erro ao criar conta: {str(e)}")

    def handle_deposit(self):
        account_id = int(input("Número da conta: "))
        amount = float(input("Valor do depósito: "))
        try:
            self.deposit_use_case.execute(account_id, amount)
            print("Depósito realizado com sucesso!")
        except Exception as e:
            print(f"Erro ao fazer depósito: {str(e)}")

    def handle_withdrawal(self):
        account_id = int(input("Número da conta: "))
        amount = float(input("Valor do saque: "))
        try:
            self.withdraw_use_case.execute(account_id, amount)
            print("Saque realizado com sucesso!")
        except Exception as e:
            print(f"Erro ao realizar saque: {str(e)}")

    def handle_transfer(self):
        source_id = int(input("Número da conta origem: "))
        dest_id = int(input("Número da conta destino: "))
        amount = float(input("Valor da transferência: "))
        try:
            self.transfer_use_case.execute(source_id, dest_id, amount)
            print("Transferência realizada com sucesso!")
        except Exception as e:
            print(f"Erro ao realizar transferência: {str(e)}")

    def handle_balance(self):
        account_id = int(input("Número da conta: "))
        try:
            # tenta usar repositório diretamente; ajuste se método tiver outro nome
            account = self.account_repo.get_by_id(account_id)
            saldo = getattr(account, "balance", "desconhecido")
            print(f"Saldo da conta {account_id}: {saldo}")
        except Exception as e:
            print(f"Erro ao consultar saldo: {str(e)}")

# compatibilidade com imports que esperam 'Menu'
Menu = BankMenu
