"""Modelo de persistência para transações financeiras.

Define a estrutura de dados para representar transações financeiras no banco de
dados SQLite, utilizando um dataclass para encapsular os atributos e métodos
associados.
"""

from dataclasses import dataclass

@dataclass
class TransactionModel:
    """Modelo de dados para uma transação financeira no banco SQLite.

    Representa os atributos de uma transação, incluindo identificador, conta
    associada, valor, tipo e data de criação.
    """
    id: int
    account_id: int
    amount: float
    type: str
    created_at: str

    @classmethod
    def from_row(cls, row: tuple) -> 'TransactionModel':
        """Cria uma instância do modelo a partir de uma linha do banco de dados.

        Args:
            row (tuple): Tupla contendo os valores (id, account_id, amount, type,
                created_at) retornados de uma consulta ao banco.

        Returns:
            TransactionModel: Instância do modelo populada com os dados da linha.
        """
        return cls(
            id=row[0],
            account_id=row[1],
            amount=row[2],
            type=row[3],
            created_at=row[4]
        )
    