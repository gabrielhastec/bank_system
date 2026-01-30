from fastapi import APIRouter, Depends
from ...application.use_cases.make_deposit import MakeDepositUseCase, DepositCommand
from ...application.use_cases.make_withdrawal import MakeWithdrawalUseCase, WithdrawalCommand
from ...application.use_cases.make_transfer import MakeTransferUseCase, TransferCommand
from ...application.use_cases.get_statement import GetStatementUseCase
from ...config.container import get_deposit_uc, get_withdrawal_uc, get_transfer_uc, get_statement_uc
from ..schemas.transaction_schema import DepositRequest, WithdrawRequest, TransferRequest, StatementResponse

router = APIRouter()

@router.post("/{account_id}/deposit")
def deposit(account_id: str, payload: DepositRequest, uc: MakeDepositUseCase = Depends(get_deposit_uc)):
    command = DepositCommand(account_id=account_id, amount=str(payload.amount))
    account = uc.execute(command)
    return {"message": "Depósito realizado com sucesso", "balance": account.balance}

@router.post("/{account_id}/withdraw")
def withdraw(account_id: str, payload: WithdrawRequest, uc: MakeWithdrawalUseCase = Depends(get_withdrawal_uc)):
    command = WithdrawalCommand(account_id=account_id, amount=str(payload.amount))
    account = uc.execute(command)
    return {"message": "Saque realizado com sucesso", "balance": account.balance}

@router.post("/{account_id}/transfer")
def transfer(account_id: str, payload: TransferRequest, uc: MakeTransferUseCase = Depends(get_transfer_uc)):
    command = TransferCommand(source_account_id=account_id, target_account_id=payload.target_account_id, amount=str(payload.amount))
    account = uc.execute(command)
    return {"message": "Transferência realizada com sucesso", "balance": account.balance}

@router.get("/{account_id}/statement", response_model=StatementResponse)
def get_statement(account_id: str, uc: GetStatementUseCase = Depends(get_statement_uc)):
    statement = uc.execute(account_id)
    return StatementResponse(transactions=statement)
