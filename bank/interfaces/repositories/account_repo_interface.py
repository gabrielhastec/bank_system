"""Interface para repositórios de usuários.

Define um contrato (protocolo) para operações de manipulação de usuários,
permitindo que casos de uso dependam de uma abstração em vez de implementações
concretas.
"""

from typing import Protocol, runtime_checkable, Optional, TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from bank.domain.entities.user import User

@runtime_checkable
class UserRepositoryInterface(Protocol):
    """Contrato para repositórios de usuários.

    Define métodos que implementações concretas devem seguir para gerenciar
    usuários no sistema, garantindo compatibilidade com os casos de uso.
    """
    
    def get_by_id(self, user_id: int) -> Optional["User"]:
        """Recupera um usuário pelo seu identificador.

        Args:
            user_id (int): Identificador do usuário a ser recuperado.

        Returns:
            Optional[User]: Instância do usuário se encontrada, ou None se não existir.
        """
        ...

    def get_by_email(self, email: str) -> Optional["User"]:
        """Recupera um usuário pelo seu endereço de e-mail.

        Args:
            email (str): Endereço de e-mail do usuário a ser recuperado.

        Returns:
            Optional[User]: Instância do usuário se encontrada, ou None se não existir.
        """
        ...

    def add(self, payload: Dict[str, Any]) -> int:
        """Insere um novo usuário no repositório.

        Args:
            payload (Dict[str, Any]): Dicionário com os dados do usuário a ser criado.

        Returns:
            int: Identificador do usuário criado.
        """
        ...

    def update(self, user_id: int, payload: Dict[str, Any]) -> None:
        """Atualiza os dados de um usuário existente.

        Args:
            user_id (int): Identificador do usuário a ser atualizado.
            payload (Dict[str, Any]): Dicionário com os dados atualizados do usuário.
        """
        ...
