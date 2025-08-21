class Transaction:
    """
    Representa uma transação bancária, como depósito ou saque.

    Attributes:
        tipo (str): Tipo da transação ('deposito' ou 'saque').
        valor (float): Valor da transação.
    """

    def __init__(self, tipo: str, valor: float):
        """
        Inicializa uma nova transação.

        Args:
            tipo (str): Tipo da transação ('deposito' ou 'saque').
            valor (float): Valor da transação.
        """
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        """
        Retorna uma representação textual da transação.

        Returns:
            str: Representação da transação.
        """
        return f"<Transaction tipo={self.tipo} valor={self.valor:.2f}>"

    def to_dict(self):
        """
        Retorna a transação como um dicionário.

        Returns:
            dict: Dicionário com os dados da transação.
        """
        return {"tipo": self.tipo, "valor": self.valor}