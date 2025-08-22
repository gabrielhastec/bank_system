from .exceptions import SaldoInsuficienteError, LimiteSaquesExcedidoError, ValorInvalidoError
from .transaction import Transaction

class Account:
    """
    Representa uma conta bancária com operações de depósito, saque e extrato.

    Attributes:
        owner (str): Nome do titular da conta.
        balance (float): Saldo atual da conta.
        saque_limite (float): Valor máximo permitido por saque.
        max_saques (int): Número máximo de saques permitidos por dia.
        saques_realizados (int): Contador de saques realizados.
        transactions (list): Lista de transações realizadas.
    """

    def __init__(self, owner, balance=0.0, saque_limite=500.0, max_saques=3):
        """
        Inicializa uma nova instância de Account.

        Args:
            owner (str): Nome do titular da conta.
            balance (float, opcional): Saldo inicial da conta. Padrão é 0.0.
            saque_limite (float, opcional): Limite de valor por saque. Padrão é 500.0.
            max_saques (int, opcional): Número máximo de saques permitidos. Padrão é 3.
        """
        self.owner = owner
        self.balance = float(balance)
        self.saque_limite = float(saque_limite)
        self.max_saques = max_saques
        self.saques_realizados = 0
        self.transactions = []

    def depositar(self, valor):
        """
        Realiza um depósito na conta.

        Args:
            valor (float): Valor a ser depositado.

        Returns:
            float: Saldo atualizado após o depósito.

        Raises:
            ValorInvalidoError: Se o valor do depósito for menor ou igual a zero.
        """
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValorInvalidoError("O valor deve ser um número válido.")
        
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        self.balance += valor
        self.transactions.append(Transaction("deposito", valor))
        return self.balance

    def sacar(self, valor):
        """
        Realiza um saque na conta.

        Args:
            valor (float): Valor a ser sacado.

        Returns:
            float: Saldo atualizado após o saque.

        Raises:
            ValorInvalidoError: Se o valor do saque for menor ou igual a zero ou exceder o limite de saque.
            SaldoInsuficienteError: Se o saldo for insuficiente para o saque.
            LimiteSaquesExcedidoError: Se o número máximo de saques for atingido.
        """
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValorInvalidoError("O valor deve ser um número válido.")
        
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if valor > self.balance:
            raise SaldoInsuficienteError("Saldo insuficiente.")
        if valor > self.saque_limite:
            raise ValorInvalidoError("Valor excede o limite de saque.")
        if self.saques_realizados >= self.max_saques:
            raise LimiteSaquesExcedidoError("Número máximo de saques atingido.")

        self.balance -= valor
        self.saques_realizados += 1
        self.transactions.append(Transaction("saque", valor))
        return self.balance

    def extrato(self):
        """
        Retorna o extrato da conta.

        Returns:
            tuple: Uma tupla contendo a lista de transações e o saldo atual.
        """
        return self.transactions, self.balance
    