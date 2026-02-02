
from fastapi import APIRouter, Depends, HTTPException, status

from ...application.use_cases.login import LoginUseCase, LoginCommand
from ...config.container import get_login_uc
from ..schemas.auth_schema import LoginRequest, LoginResponse
from ..dependencies import handle_domain_errors

router = APIRouter()

@router.post("/login", response_model=LoginResponse, summary="Autenticar usuário")
@handle_domain_errors
def login(payload: LoginRequest, uc: LoginUseCase = Depends(get_login_uc)):
    """
    Autentica um usuário e retorna um token JWT.
    
    - **cpf**: CPF do cliente (somente números)
    - **password**: Senha do cliente
    """
    try:
        # Cria comando de login
        command = LoginCommand(cpf=payload.cpf, password=payload.password)
        
        # Executa caso de uso
        result = uc.execute(command)
        
        return LoginResponse(
            token=result.token,
            account_id=result.account_id,
            name=result.name,
            cpf=result.cpf
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
@router.post("/validate", summary="Validar token JWT")
def validate_token(token: str):
    """
    Valida se um token JWT é válido.
    
    - **token**: Token JWT a ser validado
    """
    try:
        payload = JWTService.verify_token(token)
        return {
            "valid": True,
            "account_id": payload.get("sub"),
            "name": payload.get("name"),
            "expires_at": payload.get("exp")
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
