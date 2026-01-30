"""
DTO: OpenAccountDTO
-------------------
Data Transfer Object utilizado para transportar os dados necessários
para abertura de conta.

Este DTO pertence à camada de aplicação e serve apenas como estrutura
de dados simples (sem lógica de domínio), garantindo que o caso de uso
(OpenAccountUseCase) receba informações já validadas e organizadas.
"""

from dataclasses import dataclass


@dataclass
class OpenAccountDTO:
    """
    Estrutura de dados para criação de uma nova conta.

    Contém:
    - name: nome do cliente
    - email: e-mail do cliente
    - cpf: CPF em string (será convertido para Value Object posteriormente)
    - password: senha em texto claro (apenas validação mínima aqui)
    """

    name: str
    email: str
    cpf: str
    password: str

    def __post_init__(self):
        """
        Validações básicas.

        Regras:
        - A senha deve ter pelo menos 6 caracteres
        """
        if len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")
