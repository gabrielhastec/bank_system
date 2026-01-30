"""
Porta de Repositório: ICustomerRepository
-----------------------------------------
Define a interface que qualquer repositório de clientes deve implementar
(Princípio de Inversão de Dependência - camada de domínio não depende de detalhes de infraestrutura).

Esta é uma porta de saída (outbound port) do Clean Architecture / Hexagonal.
"""

from abc import ABC, abstractmethod

from ...domain.entities.customer import Customer
from ...domain.value_objects.cpf import CPF


class ICustomerRepository(ABC):
    """
    Interface para operações de persistência de clientes.
    Implementações concretas podem ser com SQLAlchemy, MongoDB, etc.
    """

    @abstractmethod
    def create(self, name: str, email: str, cpf: CPF, password_plain: str) -> Customer:
        """
        Cria um novo cliente no banco de dados.
        A senha chega em texto claro (já será hasheada na camada de domínio).
        Retorna a entidade Customer completa (com ID gerado).
        """
        ...

    @abstractmethod
    def get_by_cpf(self, cpf: CPF) -> Customer | None:
        """
        Busca um cliente pelo CPF (único no sistema).
        Retorna a entidade Customer ou None se não existir.
        """
        ...
        