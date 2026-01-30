
from unittest import result
from fastapi import APIRouter, Depends
from ...application.use_cases.login import LoginUseCase
from ...config.container import get_login_uc
from ..schemas.auth_schema import LoginRequest, LoginResponse

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    uc: LoginUseCase = Depends(get_login_uc)
):
    result = uc.execute(payload.cpf, payload.password)

    return LoginResponse(
        token=result.token,
        account_id=result.account_id,
        name=result.name
    )
