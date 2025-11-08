from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from bank.domain.entities.account import Account
from bank.infrastructure.utils.validators import validate_name, validate_cpf, validate_email
from bank.domain.exceptions import InvalidAmountError, DuplicateAccountError

"""
Módulo que define a classe User para gerenciamento de usuários do sistema bancário.

A classe User representa o titular de uma ou mais contas, contendo informações pessoais
e métodos utilitários para gerenciamento e serialização de dados do usuário.
"""

@dataclass
class User:
    """Classe que representa um usuário do sistema bancário.

    Atributos:
        id (int): Identificador único do usuário.
        name (str): Nome completo do usuário.
        cpf (str): CPF do usuário, validado no formato correto.
        email (str): Endereço de e-mail do usuário.
        created_at (datetime): Data de criação do registro.
        accounts (List[Account]): Lista de contas associadas ao usuário.
    """
    id: int
    name: str
    cpf: str
    email: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    accounts: List[Account] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Valida os atributos após a inicialização do objeto.

        Raises:
            ValorInvalidoError: Se algum campo obrigatório for inválido.
        """
        validate_name(self.name)
        validate_cpf(self.cpf)
        validate_email(self.email)
        if self.id <= 0:
            raise InvalidAmountError("ID do usuário deve ser positivo.")

    def add_account(self, account: Account) -> None:
        """Associa uma nova conta a este usuário.

        Args:
            account (Account): Objeto da conta a ser adicionada.

        Raises:
            ValorInvalidoError: Se a conta já estiver associada.
        """
        if any(acc.id == account.id for acc in self.accounts):
            raise DuplicateAccountError(f"A conta {account.id} já está associada a este usuário.")
        self.accounts.append(account)

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """Retorna uma conta associada ao usuário pelo ID.

        Args:
            account_id (int): Identificador da conta buscada.

        Returns:
            Optional[Account]: Objeto da conta, se encontrado; caso contrário, None.
        """
        return next((acc for acc in self.accounts if acc.id == account_id), None)
