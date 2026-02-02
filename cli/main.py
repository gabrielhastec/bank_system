"""
CLI Completa: Interface de Linha de Comando do Sistema Bancário
---------------------------------------------------------------
Interface completa com todas as funcionalidades:
- Abertura de conta
- Login
- Depósito
- Saque
- Transferência
- Extrato
"""

import sys
import os
import json
from decimal import Decimal
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.src.config.container import container
from backend.src.application.dto.open_account_dto import OpenAccountDTO
from backend.src.domain.value_objects.cpf import CPF
from backend.src.domain.exceptions import (
    DuplicateCPFException, 
    InsufficientFunds, 
    DailyLimitExceeded
)


class BankingCLI:
    """Classe principal da CLI"""
    
    def __init__(self):
        self.current_account_id: Optional[str] = None
        self.current_customer_name: Optional[str] = None
        self.container = container
    
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Imprime cabeçalho formatado"""
        self.clear_screen()
        print("=" * 50)
        print(f"{title:^50}")
        print("=" * 50)
        print()
    
    def wait_for_enter(self):
        """Aguarda Enter para continuar"""
        input("\nPressione Enter para continuar...")
    
    def show_main_menu(self):
        """Exibe menu principal"""
        while True:
            self.print_header("BANCO DIGITAL - MENU PRINCIPAL")
            
            if self.current_account_id:
                print(f"👤 Logado como: {self.current_customer_name}")
                print(f"📋 Conta: {self.current_account_id[:8]}...")
                print()
            
            print("1. Criar nova conta")
            print("2. Login")
            
            if self.current_account_id:
                print("3. Realizar depósito")
                print("4. Realizar saque")
                print("5. Realizar transferência")
                print("6. Ver extrato")
                print("7. Logout")
            
            print("0. Sair")
            print()
            
            choice = input("Escolha uma opção: ").strip()
            
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "3" and self.current_account_id:
                self.make_deposit()
            elif choice == "4" and self.current_account_id:
                self.make_withdrawal()
            elif choice == "5" and self.current_account_id:
                self.make_transfer()
            elif choice == "6" and self.current_account_id:
                self.get_statement()
            elif choice == "7" and self.current_account_id:
                self.logout()
            elif choice == "0":
                print("\nObrigado por usar o Banco Digital!")
                break
            else:
                print("\n❌ Opção inválida!")
                self.wait_for_enter()
    
    def create_account(self):
        """Cria uma nova conta"""
        self.print_header("CRIAR NOVA CONTA")
        
        print("Preencha os dados para criar sua conta:")
        print()
        
        name = input("Nome completo: ").strip()
        email = input("Email: ").strip()
        cpf = input("CPF (somente números): ").strip()
        password = input("Senha (mínimo 6 caracteres): ").strip()
        
        # Validação básica
        if len(password) < 6:
            print("\n❌ A senha deve ter pelo menos 6 caracteres.")
            self.wait_for_enter()
            return
        
        try:
            # Valida CPF
            CPF(cpf)
        except ValueError:
            print("\n❌ CPF inválido.")
            self.wait_for_enter()
            return
        
        # Obtém o caso de uso
        uc = self.container.open_account_uc()
        
        try:
            dto = OpenAccountDTO(
                name=name,
                email=email,
                cpf=cpf,
                password=password,
            )
            
            account = uc.execute(dto)
            
            print("\n✅ CONTA CRIADA COM SUCESSO!")
            print(f"Número da conta: {account.account_id}")
            print(f"Titular: {account.customer.name}")
            print(f"CPF: {account.customer.cpf}")
            print(f"Saldo inicial: R$ 0,00")
            print("\n⚠️  Guarde o número da conta para login!")
            
        except DuplicateCPFException as e:
            print(f"\n❌ {e}")
        except ValueError as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
        
        self.wait_for_enter()
    
    def login(self):
        """Realiza login na conta"""
        self.print_header("LOGIN")
        
        cpf = input("CPF (somente números): ").strip()
        password = input("Senha: ").strip()
        
        # Obtém o caso de uso de login
        uc = self.container.login_uc()
        
        try:
            result = uc.execute(cpf, password)
            
            self.current_account_id = result["account_id"]
            self.current_customer_name = result["name"]
            
            print("\n✅ LOGIN REALIZADO COM SUCESSO!")
            print(f"Bem-vindo(a), {result['name']}!")
            print(f"Conta: {result['account_id']}")
            
        except ValueError as e:
            print(f"\n❌ {e}")
        
        self.wait_for_enter()
    
    def make_deposit(self):
        """Realiza um depósito"""
        self.print_header("REALIZAR DEPÓSITO")
        
        print(f"Conta: {self.current_account_id}")
        print(f"Titular: {self.current_customer_name}")
        print()
        
        amount = input("Valor do depósito (R$): ").strip().replace(",", ".")
        
        try:
            # Valida o valor
            amount_decimal = Decimal(amount)
            if amount_decimal <= 0:
                print("\n❌ O valor deve ser positivo.")
                self.wait_for_enter()
                return
        except:
            print("\n❌ Valor inválido.")
            self.wait_for_enter()
            return
        
        # Obtém o caso de uso
        uc = self.container.deposit_uc()
        
        try:
            from backend.src.application.use_cases.make_deposit import DepositCommand
            command = DepositCommand(
                account_id=self.current_account_id,
                amount=amount
            )
            
            account = uc.execute(command)
            
            print(f"\n✅ DEPÓSITO REALIZADO COM SUCESSO!")
            print(f"Novo saldo: {account.balance}")
            
        except ValueError as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        
        self.wait_for_enter()
    
    def make_withdrawal(self):
        """Realiza um saque"""
        self.print_header("REALIZAR SAQUE")
        
        print(f"Conta: {self.current_account_id}")
        print(f"Titular: {self.current_customer_name}")
        print()
        print("⚠️  Limites diários:")
        print("   • Valor máximo: R$ 3.000,00")
        print("   • Quantidade máxima: 5 saques")
        print()
        
        amount = input("Valor do saque (R$): ").strip().replace(",", ".")
        
        try:
            amount_decimal = Decimal(amount)
            if amount_decimal <= 0:
                print("\n❌ O valor deve ser positivo.")
                self.wait_for_enter()
                return
        except:
            print("\n❌ Valor inválido.")
            self.wait_for_enter()
            return
        
        # Obtém o caso de uso
        uc = self.container.withdrawal_uc()
        
        try:
            from backend.src.application.use_cases.make_withdrawal import WithdrawalCommand
            command = WithdrawalCommand(
                account_id=self.current_account_id,
                amount=amount
            )
            
            account = uc.execute(command)
            
            print(f"\n✅ SAQUE REALIZADO COM SUCESSO!")
            print(f"Novo saldo: {account.balance}")
            
        except InsufficientFunds as e:
            print(f"\n❌ {e}")
        except DailyLimitExceeded as e:
            print(f"\n❌ {e}")
        except ValueError as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        
        self.wait_for_enter()
    
    def make_transfer(self):
        """Realiza uma transferência"""
        self.print_header("REALIZAR TRANSFERÊNCIA")
        
        print(f"Conta origem: {self.current_account_id}")
        print(f"Titular: {self.current_customer_name}")
        print()
        
        target_account_id = input("Número da conta destino: ").strip()
        amount = input("Valor da transferência (R$): ").strip().replace(",", ".")
        
        try:
            amount_decimal = Decimal(amount)
            if amount_decimal <= 0:
                print("\n❌ O valor deve ser positivo.")
                self.wait_for_enter()
                return
        except:
            print("\n❌ Valor inválido.")
            self.wait_for_enter()
            return
        
        # Obtém o caso de uso
        uc = self.container.transfer_uc()
        
        try:
            from backend.src.application.use_cases.make_transfer import TransferCommand
            command = TransferCommand(
                source_account_id=self.current_account_id,
                target_account_id=target_account_id,
                amount=amount
            )
            
            result = uc.execute(command)
            
            print(f"\n✅ TRANSFERÊNCIA REALIZADA COM SUCESSO!")
            print(f"Novo saldo: {result.balance}")
            
        except InsufficientFunds as e:
            print(f"\n❌ {e}")
        except DailyLimitExceeded as e:
            print(f"\n❌ {e}")
        except ValueError as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        
        self.wait_for_enter()
    
    def get_statement(self):
        """Exibe o extrato da conta"""
        self.print_header("EXTRATO DA CONTA")
        
        print(f"Conta: {self.current_account_id}")
        print(f"Titular: {self.current_customer_name}")
        print()
        
        # Obtém o caso de uso
        uc = self.container.statement_uc()
        
        try:
            statement = uc.execute(self.current_account_id)
            
            if not statement:
                print("📭 Nenhuma transação encontrada.")
            else:
                print("📋 ÚLTIMAS TRANSAÇÕES:")
                print("-" * 60)
                
                for i, transaction in enumerate(statement, 1):
                    tipo = {
                        "deposit": "💰 DEPÓSITO",
                        "withdrawal": "💳 SAQUE",
                        "transfer": "🔄 TRANSFERÊNCIA"
                    }.get(transaction["type"], transaction["type"].upper())
                    
                    amount = transaction["amount"]
                    date = transaction["occurred_at"]
                    
                    print(f"{i:2}. {tipo:20} {amount:>15}   {date}")
                
                print("-" * 60)
            
        except ValueError as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        
        self.wait_for_enter()
    
    def logout(self):
        """Realiza logout"""
        self.current_account_id = None
        self.current_customer_name = None
        print("\n✅ Logout realizado com sucesso!")
        self.wait_for_enter()


def main():
    """Função principal"""
    from backend.src.infrastructure.database.orm import init_db
    
    # Inicializa o banco de dados
    init_db()
    
    # Inicia a CLI
    cli = BankingCLI()
    cli.show_main_menu()


if __name__ == "__main__":
    main()
    