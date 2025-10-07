from datetime import datetime
from bank.domain.entities.account import Account
from bank.domain.entities.user import User
from bank.interfaces.repositories.account_repo_interface import AccountRepositoryInterface
from bank.interfaces.repositories.user_repo_interface import UserRepositoryInterface
from bank.exceptions import ValorInvalidoError

"""
Caso de uso responsável pela abertura de uma nova conta para um usuário existente.
"""

class OpenAccountUseCase:
    """Caso de uso para abertura de conta bancária."""

    def __init__(self, account_repo: AccountRepositoryInterface, user_repo: UserRepositoryInterface):
        """Inicializa o caso de uso com os repositórios necessários.

        Args:
            account_repo (AccountRepositoryInterface): Repositório de contas.
            user_repo (UserRepositoryInterface): Repositório de usuários.
        """
        self.account_repo = account_repo
        self.user_repo = user_repo

    def execute(self, user_id: int, initial_deposit: float = 0.0) -> Account:
        """Cria uma nova conta associada a um usuário existente.

        Args:
            user_id (int): Identificador do usuário dono da conta.
            initial_deposit (float, optional): Valor inicial do depósito. Padrão é 0.0.

        Returns:
            Account: Objeto da conta criada.
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValorInvalidoError("Usuário não encontrado.")

        # Criação da nova conta
        new_account = Account(
            id=self.account_repo.get_next_id(),
            cpf=user.cpf,
            name=user.name,
            balance=initial_deposit
        )

        # Persistência da nova conta e atualização do usuário
        self.account_repo.add(new_account)
        user.add_account(new_account)
        self.user_repo.update(user)

        return new_account
