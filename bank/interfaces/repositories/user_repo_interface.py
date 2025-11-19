"""Interface para repositórios de usuários.

Define um contrato (protocolo) para operações de manipulação de usuários,
permitindo que casos de uso dependam de uma abstração em vez de implementações
concretas.
"""

from typing import Protocol, runtime_checkable, Optional, TYPE_CHECKING, Dict, Any
from bank.domain.exceptions import UserNotFoundError, InvalidEmailError

if TYPE_CHECKING:
    from bank.domain.entities.user import User

@runtime_checkable
class UserRepositoryInterface(Protocol):
    """Contrato para repositórios de usuários."""
    def get_by_id(self, user_id: int) -> Optional["User"]:
        """Recupera um usuário pelo seu identificador.

        Raises:
            UserNotFoundError: se o usuário não for encontrado.
        """
        ...

    def get_by_email(self, email: str) -> Optional["User"]:
        """Recupera um usuário pelo seu endereço de e-mail.

        Raises:
            InvalidEmailError: se o e-mail informado for inválido.
        """
        ...

    def add(self, payload: Dict[str, Any]) -> int:
        """Insere um novo usuário no repositório.

        Raises:
            InvalidEmailError: se o e-mail for inválido.
            ValueError: se payload estiver incompleto.
        """
        ...

    def update(self, user_id: int, payload: Dict[str, Any]) -> None:
        """Atualiza os dados de um usuário existente.

        Raises:
            UserNotFoundError: se o usuário não existir.
            InvalidEmailError: se o e-mail for inválido no payload.
        """
        ...
