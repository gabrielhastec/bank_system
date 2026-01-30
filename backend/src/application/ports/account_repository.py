
from abc import ABC, abstractmethod

from ...domain.entities.account import Account

class IAccountRepository(ABC):
    @abstractmethod
    def save(self, account: Account) -> None: ...

    @abstractmethod
    def get_by_id(self, account_id: str) -> Account | None: ...

    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Account | None: ... 
