"""
Schemas de Autenticação
-----------------------
"""
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    """Schema para requisição de login."""
    cpf: str = Field(..., example="12345678900", description="CPF do cliente")
    password: str = Field(..., example="minhasenha123", description="Senha do cliente")

class LoginResponse(BaseModel):
    """Schema para resposta de login."""
    token: str = Field(..., description="Token JWT de acesso")
    account_id: str = Field(..., description="ID da conta do cliente")
    name: str = Field(..., description="Nome do cliente")
    cpf: str = Field(..., description="CPF formatado do cliente")

class TokenData(BaseModel):
    """Dados contidos no token JWT."""
    account_id: str
    name: str
    cpf: str
