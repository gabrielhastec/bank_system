
from dataclasses import dataclass
import jwt
from datetime import datetime, timedelta

from backend.src.domain.value_objects.cpf import CPF
from backend.src.config.settings import settings
from backend.src.application.ports.customer_repository import ICustomerRepository
from backend.src.application.ports.account_repository import IAccountRepository

@dataclass
class LoginCommand:
    cpf: str
    password: str

@dataclass
class LoginResult:
    token: str
    account_id: str
    name: str
    cpf: str

class LoginUseCase:

    def __init__(self, customer_repo: ICustomerRepository, account_repo: IAccountRepository):
        self.customer_repo = customer_repo
        self.account_repo = account_repo

    def execute(self, command: LoginCommand):

        # Valida CPF
        cpf = CPF(command.cpf)

        # Busca cliente pelo CPF
        customer = self.customer_repo.get_by_cpf(cpf)
        if not customer:
            raise ValueError("CPF ou senha inválidos")
        
        # Verifica senha
        if not customer.verify_password(command.password):
            raise ValueError("CPF ou senha inválidos")
        
        # Busca conta associada ao cliente
        account = self.account_repo.get_by_cpf(cpf)
        if not account:
            raise ValueError("Conta não encontrada para este CPF")
        
        # Gera token JWT
        token_data = {
            "sub": account.account_id,
            "name": customer.name,
            "cpf": str(customer.cpf),
            "iat": datetime.utcnow(),
            "account_id": account.account_id
        }

        token = jwt.encode(
            token_data,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        
        return LoginResult(
            token=token,
            account_id=account.account_id,
            name=customer.name,
            cpf=str(customer.cpf)
        )
    