"""Interface para repositórios de usuários e contas.

Define um contrato (protocolo) para operações de manipulação de usuários e contas,
permitindo que casos de uso dependam de uma abstração em vez de implementações
concretas.
"""

from typing import Protocol, runtime_checkable, Optional, TYPE_CHECKING, Dict, Any, List
from bank.domain.exceptions import InvalidAccountError, UserNotFoundError

if TYPE_CHECKING:
    from bank.domain.entities.user import User
    from bank.domain.entities.account import Account

@runtime_checkable
class UserRepositoryInterface(Protocol):
    """Contrato para repositórios de usuários."""
    def get_by_id(self, user_id: int) -> Optional["User"]:
        """Recupera um usuário pelo seu identificador.

        Raises:
            UserNotFoundError: se o usuário não existir.
        """
        ...

    def get_by_email(self, email: str) -> Optional["User"]:
        """Recupera um usuário pelo seu endereço de e-mail."""
        ...

    def add(self, payload: Dict[str, Any]) -> int:
        """Insere um novo usuário no repositório.

        Raises:
            ValueError: se payload estiver incompleto ou inválido.
        """
        ...

    def update(self, user_id: int, payload: Dict[str, Any]) -> None:
        """Atualiza os dados de um usuário existente.

        Raises:
            UserNotFoundError: se o usuário não existir.
            ValueError: se payload for inválido.
        """
        ...

@runtime_checkable
class AccountRepositoryInterface(Protocol):
    """Contrato para repositórios de contas usado pelos usecases."""
    def get_by_id(self, account_id: int) -> Optional["Account"]:
        """Retorna a Account ou None se não existir.

        Raises:
            InvalidAccountError: se account_id for inválido.
        """
        ...
    
    def add(self, payload: Dict[str, Any]) -> int:
        """Cria conta e retorna id.

        Raises:
            UserNotFoundError: se o usuário associado não existir.
            ValueError: se payload inválido.
        """
        ...
    
    def update(self, account_id: int, payload: Dict[str, Any]) -> None:
        """Atualiza dados da conta (saldo, status, etc.).

        Raises:
            InvalidAccountError: se a conta não existir.
            ValueError: se os dados forem inválidos.
        """
        ...
    
    def list_by_user(self, user_id: int) -> List["Account"]:
        """Retorna lista de contas de um usuário.

        Raises:
            UserNotFoundError: se o usuário não existir.
        """
        ...
