"""
Schemas da API: AccountCreateRequest & AccountResponse
-----------------------------------------------------
Responsáveis por validar dados de entrada/saída no nível da API
utilizando Pydantic.

Estes schemas pertencem à camada de Interface (Delivery Layer) da
Clean Architecture. Eles não contêm lógica de domínio, apenas
transformam dados entre:
- JSON da requisição
- DTOs da camada de aplicação
- Entidades/aggregates para resposta HTTP
"""

from pydantic import BaseModel, Field
from ...application.dto.open_account_dto import OpenAccountDTO
from ...domain.entities.account import Account

class AccountCreateRequest(BaseModel):
    """
    Schema de entrada para criação de conta via API.

    Responsável por:
    - Validar os campos enviados no corpo da requisição
    - Transformar esses dados em um DTO (OpenAccountDTO)
    """
    name: str = Field(..., example="Gabriel Rodrigues")
    email: str = Field(..., example="gabriel@email.com")
    cpf: str = Field(..., example="12345678900")
    password: str = Field(..., example="minhasenha123")

    def to_dto(self) -> OpenAccountDTO:
        """
        Converte os dados validados do request para o DTO
        usado pelo caso de uso OpenAccountUseCase.
        """
        return OpenAccountDTO(
            name=self.name,
            email=self.email,
            cpf=self.cpf,
            password=self.password
        )

class AccountResponse(BaseModel):
    """
    Schema de saída da API para retornar informações de uma conta criada.

    Este schema é construído a partir de uma entidade/aggregate
    e exposto como resposta JSON ao cliente.
    """

    account_id: str
    name: str
    cpf: str

    @staticmethod
    def from_domain(account: Account):
        """
        Converte a entidade/aggregate de domínio Account
        para o formato esperado pela API.
        """
        return AccountResponse(
            account_id=account.account_id,
            name=account.customer.name,
            cpf=str(account.customer.cpf)
        )

class LoginRequest(BaseModel):
    cpf: str
    password: str

class LoginResponse(BaseModel):
    token: str
    account_id: str
    name: str
