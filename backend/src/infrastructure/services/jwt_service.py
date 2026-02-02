"""
Serviço JWT para autenticação
------------------------------
Responsável por gerar e validar tokens JWT para autenticação.
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from ...config.settings import settings

class JWTService:
    """Serviço para manipulação de tokens JWT."""
    
    @staticmethod
    def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Cria um token JWT de acesso.
        
        Args:
            data: Dados a serem incluídos no token
            expires_delta: Tempo de expiração do token
            
        Returns:
            Token JWT assinado
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.jwt_expiration_minutes
            )
            
        to_encode.update({"exp": expire, "type": "access"})
        
        return jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
    
    @staticmethod
    def verify_token(token: str) -> Dict:
        """
        Verifica e decodifica um token JWT.
        
        Args:
            token: Token JWT a ser verificado
            
        Returns:
            Payload decodificado
            
        Raises:
            ValueError: Se o token for inválido ou expirado
        """
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )
            
            if payload.get("type") != "access":
                raise ValueError("Tipo de token inválido")
                
            return payload
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Token inválido: {str(e)}")
    
    @staticmethod
    def extract_account_id(token: str) -> str:
        """
        Extrai o ID da conta de um token JWT.
        
        Args:
            token: Token JWT
            
        Returns:
            ID da conta
        """
        payload = JWTService.verify_token(token)

        return payload.get("sub", payload.get("account_id"))
