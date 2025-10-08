"""Modelo de persistência para contas bancárias.

Define a estrutura de dados para representar contas bancárias no banco de dados
SQLite, utilizando um dataclass para encapsular os atributos e métodos associados.
"""

from dataclasses import dataclass

@dataclass
class AccountModel:
    """Modelo de dados para uma conta bancária no banco SQLite.

    Representa os atributos de uma conta, incluindo identificador, usuário associado
    e saldo.
    """
    id: int
    user_id: int
    balance: float

    @classmethod
    def from_row(cls, row: tuple) -> 'AccountModel':
        """Cria uma instância do modelo a partir de uma linha do banco de dados.

        Args:
            row (tuple): Tupla contendo os valores (id, user_id, balance) retornados
                de uma consulta ao banco.

        Returns:
            AccountModel: Instância do modelo populada com os dados da linha.
        """
        return cls(id=row[0], user_id=row[1], balance=row[2])
    