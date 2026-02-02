"""
Dependências do FastAPI e Middlewares
-------------------------------------
"""

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from ..domain.exceptions import (
    DomainException, InsufficientFunds, 
    DailyLimitExceeded, DuplicateCPFException
)
from ..infrastructure.services.jwt_service import JWTService

# Esquema de autenticação Bearer
security = HTTPBearer()

def get_current_account(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependência para obter a conta atual a partir do token JWT.
    
    Args:
        credentials: Credenciais Bearer HTTP
        
    Returns:
        Dados da conta autenticada
        
    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    token = credentials.credentials
    
    try:
        payload = JWTService.verify_token(token)
        return {
            "account_id": payload.get("sub") or payload.get("account_id"),
            "name": payload.get("name"),
            "cpf": payload.get("cpf")
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def require_same_account(account_id: str, current_account: dict = Depends(get_current_account)):
    """
    Dependência para verificar se o usuário acessa apenas sua própria conta.
    
    Args:
        account_id: ID da conta a ser acessada
        current_account: Dados da conta autenticada
        
    Raises:
        HTTPException: Se tentar acessar conta diferente da sua
    """
    if current_account["account_id"] != account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a acessar esta conta"
        )
    
    return current_account

def handle_domain_errors(func):
    """
    Decorator para converter exceções de domínio em respostas HTTP apropriadas.
    """
    from functools import wraps
    from fastapi import HTTPException
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        
        except InsufficientFunds as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
                headers={"X-Error-Type": "insufficient_funds"}
            )
        
        except DailyLimitExceeded as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
                headers={"X-Error-Type": "daily_limit_exceeded"}
            )
        
        except DuplicateCPFException as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
                headers={"X-Error-Type": "duplicate_cpf"}
            )
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        except Exception as e:
            # Logar erro interno
            import logging
            logging.error(f"Erro interno: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    return wrapper
