from bank.services.account_service import AccountService
from bank.core.schema import create_tables
from bank.utils.validators import ensure_cpf_format
import sys

"""Módulo que define a classe Menu para interface CLI de um sistema bancário.

Fornece uma interface de linha de comando para criar contas, buscar contas, realizar
depósitos, saques, transferências e consultar extratos, utilizando o AccountService.
"""

class Menu:
    """Classe para interface de linha de comando do sistema bancário.

    Inicializa o banco de dados e fornece um menu interativo para gerenciar contas
    e transações por meio do AccountService.
    """

    def __init__(self) -> None:
        """Inicializa o menu, criando o esquema do banco de dados e instanciando o serviço."""
        create_tables()
        self.service = AccountService()

    def run(self) -> None:
        """Executa o loop principal do menu interativo.

        Exibe opções para o usuário e chama os métodos correspondentes com base na escolha.
        O loop termina quando o usuário seleciona a opção de sair.
        """
        while True:
            print("\n=== Bank System CLI ===")
            print("1) Criar conta")
            print("2) Buscar conta por CPF")
            print("3) Depositar")
            print("4) Sacar")
            print("5) Transferir")
            print("6) Extrato")
            print("7) Sair")
            op = input("Escolha: ").strip()
            try:
                if op == "1":
                    self.create_account()
                elif op == "2":
                    self.find_account()
                elif op == "3":
                    self.deposit()
                elif op == "4":
                    self.withdraw()
                elif op == "5":
                    self.transfer()
                elif op == "6":
                    self.statement()
                elif op == "7":
                    print("Saindo...")
                    break
                else:
                    print("Opção inválida.")
            except Exception as e:
                print(f"Erro: {e}")

    def create_account(self) -> None:
        """Cria uma nova conta com base em CPF e nome fornecidos pelo usuário.

        Solicita o CPF e nome, valida o CPF e exibe os detalhes da conta criada.
        """
        cpf = input("CPF: ")
        cpf = ensure_cpf_format(cpf)
        name = input("Nome: ")
        acc = self.service.create_account(cpf=cpf, name=name)
        print(f"Conta criada: ID={acc.id} CPF={acc.cpf} Nome={acc.name}")

    def find_account(self) -> None:
        """Busca uma conta pelo CPF e exibe suas informações.

        Solicita o CPF, valida-o e exibe os detalhes da conta, se encontrada.
        """
        cpf = ensure_cpf_format(input("CPF: "))
        acc = self.service.repo.get_account_by_cpf(cpf)
        if not acc:
            print("Conta não encontrada.")
        else:
            print(f"ID: {acc.id} | CPF: {acc.cpf} | Nome: {acc.name} | Saldo: R${acc.balance:.2f}")

    def deposit(self) -> None:
        """Realiza um depósito em uma conta.

        Solicita o ID da conta e o valor, realiza o depósito e confirma a operação.

        Raises:
            ValueError: Se o valor ou ID for inválido.
            ContaNaoEncontradaError: Se a conta não for encontrada.
            ValorInvalidoError: Se o valor não for positivo.
        """
        acc_id = int(input("ID da conta: "))
        amount = input("Valor: ")
        self.service.deposit(acc_id, amount)
        print("Depósito realizado.")

    def withdraw(self) -> None:
        """Realiza um saque de uma conta.

        Solicita o ID da conta e o valor, realiza o saque e confirma a operação.

        Raises:
            ValueError: Se o valor ou ID for inválido.
            ContaNaoEncontradaError: Se a conta não for encontrada.
            ValorInvalidoError: Se o valor não for positivo.
            SaldoInsuficienteError: Se o saldo for insuficiente.
        """
        acc_id = int(input("ID da conta: "))
        amount = input("Valor: ")
        self.service.withdraw(acc_id, amount)
        print("Saque realizado.")

    def transfer(self) -> None:
        """Realiza uma transferência entre duas contas.

        Solicita os IDs da conta de origem e destino, o valor, realiza a transferência
        e confirma a operação.

        Raises:
            ValueError: Se o valor ou IDs forem inválidos.
            ContaNaoEncontradaError: Se uma das contas não for encontrada.
            ValorInvalidoError: Se o valor não for positivo.
            SaldoInsuficienteError: Se o saldo da conta de origem for insuficiente.
        """
        src = int(input("ID origem: "))
        tgt = int(input("ID destino: "))
        amount = input("Valor: ")
        self.service.transfer(src, tgt, amount)
        print("Transferência realizada.")

    def statement(self) -> None:
        """Exibe o extrato de transações de uma conta.

        Solicita o ID da conta e exibe todas as transações associadas, se houver.
        """
        acc_id = int(input("ID da conta: "))
        rows = self.service.get_statement(acc_id)
        if not rows:
            print("Nenhuma transação.")
            return
        for r in rows:
            print(f"[{r.timestamp}] {r.type}: R$ {r.amount:.2f}")
