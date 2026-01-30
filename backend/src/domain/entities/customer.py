"""
Entidade Customer
-----------------
Representa um cliente no domínio da aplicação.
É uma entidade imutável (frozen) com identidade própria (customer_id).
A senha nunca é guardada em texto claro — só o hash.
"""

from dataclasses import dataclass, field
from typing import Optional
import uuid

from ...domain.value_objects.cpf import CPF
from ...domain.value_objects.password import Password


@dataclass(frozen=True, slots=True)
class Customer:
    """Cliente do sistema."""
    
    name: str
    email: str
    cpf: CPF
    customer_id: str = field(default_factory=lambda: str(uuid.uuid4()))  # UUID único da entidade
    _password: Optional[Password] = None  # só guarda o hash da senha

    @classmethod
    def create(cls, name: str, email: str, cpf: str, plain_password: str) -> "Customer":
        """
        Forma recomendada de criar um Customer.
        Já valida o CPF e faz o hash da senha automaticamente.
        """
        pwd = Password.create(plain_password)   # hash da senha
        cpf_vo = CPF(cpf)                        # valida e encapsula o CPF
        return cls(name=name, email=email, cpf=cpf_vo, _password=pwd)

    def verify_password(self, plain_password: str) -> bool:
        """Compara a senha informada com o hash armazenado."""
        if not self._password:
            return False
        return self._password.verify(plain_password)
    