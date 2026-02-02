
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ...application.use_cases.make_deposit import MakeDepositUseCase, DepositCommand
from ...application.use_cases.make_withdrawal import MakeWithdrawalUseCase, WithdrawalCommand
from ...application.use_cases.make_transfer import MakeTransferUseCase, TransferCommand
from ...application.use_cases.get_statement import GetStatementUseCase
from ...config.container import get_deposit_uc, get_withdrawal_uc, get_transfer_uc, get_statement_uc
from ..schemas.transaction_schema import DepositRequest, WithdrawRequest, TransferRequest, StatementResponse, TransactionResponse
from ..dependencies import get_current_account, require_same_account, handle_domain_errors

router = APIRouter()

@router.post("/{account_id}/deposit", summary="Realizar depósito")
@handle_domain_errors
def deposit(
    account_id: str, 
    payload: DepositRequest, 
    uc: MakeDepositUseCase = Depends(get_deposit_uc),
    current_account: dict = Depends(require_same_account)
):
    """
    Realiza um depósito na conta especificada.
    
    - **account_id**: ID da conta
    - **amount**: Valor do depósito (deve ser positivo)
    """
    command = DepositCommand(account_id=account_id, amount=str(payload.amount))
    account = uc.execute(command)

    return {
        "message": "Depósito realizado com sucesso",
        "balance": str(account.balance),
        "transaction_id": account.transactions[-1]["transaction_id"] if account.transactions else None
    }

@router.post("/{account_id}/withdraw", summary="Realizar saque")
@handle_domain_errors
def withdraw(
    account_id: str, 
    payload: WithdrawRequest, 
    uc: MakeWithdrawalUseCase = Depends(get_withdrawal_uc),
    current_account: dict = Depends(require_same_account)
):
    """
    Realiza um saque na conta especificada.
    
    - **account_id**: ID da conta
    - **amount**: Valor do saque (deve ser positivo e respeitar limites)
    """
    command = WithdrawalCommand(account_id=account_id, amount=str(payload.amount))
    account = uc.execute(command)

    return {
        "message": "Saque realizado com sucesso",
        "balance": str(account.balance),
        "daily_withdrawals_count": account.daily_withdrawal_count,
        "daily_withdrawals_amount": str(account.daily_withdrawal_amount),
        "transaction_id": account.transactions[-1]["transaction_id"] if account.transactions else None
    }

@router.post("/{account_id}/transfer", summary="Realizar transferência")
@handle_domain_errors
def transfer(
    account_id: str, 
    payload: TransferRequest, 
    uc: MakeTransferUseCase = Depends(get_transfer_uc),
    current_account: dict = Depends(require_same_account)
):
    """
    Realiza uma transferência da conta especificada para outra conta.
    
    - **account_id**: ID da conta de origem
    - **target_account_id**: ID da conta de destino
    - **amount**: Valor da transferência (deve ser positivo)
    """
    command = TransferCommand(
        source_account_id=account_id,
        target_account_id=payload.target_account_id,
        amount=str(payload.amount)
    )
    result = uc.execute(command)

    return {
        "message": "Transferência realizada com sucesso",
        "source_balance": str(result["source_account"].balance),
        "target_account_id": payload.target_account_id,
        "transaction_ids": {
            "withdrawal": result.get("withdrawal_transaction_id"),
            "deposit": result.get("deposit_transaction_id")
        }
    }

@router.get("/{account_id}/statement", 
           response_model=StatementResponse, 
           summary="Obter extrato")
@handle_domain_errors
def get_statement(
    account_id: str, 
    uc: GetStatementUseCase = Depends(get_statement_uc),
    current_account: dict = Depends(require_same_account)
):
    """
    Obtém o extrato de transações da conta especificada.
    
    - **account_id**: ID da conta
    """
    statement = uc.execute(account_id)
    return StatementResponse(transactions=statement)
