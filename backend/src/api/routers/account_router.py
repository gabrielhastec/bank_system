

from fastapi import APIRouter, Depends
from ..schemas.account_schema import AccountCreateRequest, AccountResponse
from ...application.use_cases.open_account import OpenAccountUseCase
from ...config.container import get_open_account_uc

router = APIRouter()

@router.post("/", response_model=AccountResponse, status_code=201)
def open_account(
    payload: AccountCreateRequest, 
    uc: OpenAccountUseCase = Depends(get_open_account_uc)
):
    result = uc.execute(payload.to_dto())
    return AccountResponse.from_domain(result)
