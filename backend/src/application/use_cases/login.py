
from dataclasses import dataclass

from ...domain.value_objects.cpf import CPF
from ..ports.customer_repository import ICustomerRepository
from ..ports.account_repository import IAccountRepository

@dataclass
class LoginCommand:
    cpf: str
    password: str

class LoginUseCase:
    def __init__(self, customer_repo: ICustomerRepository, account_repo: IAccountRepository):
        self.customer_repo = customer_repo
        self.account_repo = account_repo

    def execute(self, command: LoginCommand):
        cpf = CPF(command.cpf)
        customer = self.customer_repo.get_by_cpf(cpf)
        if not customer:
            raise ValueError("CPF ou senha inválidos")
        
        if not customer.verify_password(command.password):
            raise ValueError("CPF ou senha inválidos")
        
        # Aqui, precisaríamos de um token JWT ou similar. Por enquanto, retornaremos o account_id.
        # Vamos supor que o customer tem uma conta. Precisamos buscar a conta pelo CPF? 
        # Não temos esse método no account_repo. Vamos adicionar?
        # Ou podemos mudar: o login retorna o customer e depois o frontend busca a conta?
        # Por simplicidade, vamos retornar o customer e o account_id.
        # Mas note: um CPF pode ter apenas uma conta? No nosso sistema, sim.
        # Então, vamos adicionar um método no account_repo para buscar por CPF.
        account = self.account_repo.get_by_cpf(cpf)
        if not account:
            raise ValueError("Conta não encontrada para este CPF")
        
        # Gerar token JWT? Por enquanto, retornaremos os dados.
        return {
            "account_id": account.account_id,
            "name": customer.name,
            "cpf": str(customer.cpf)
        }
    