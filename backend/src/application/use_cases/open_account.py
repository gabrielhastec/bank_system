"""
Caso de Uso: OpenAccountUseCase
-------------------------------

Este módulo implementa o caso de uso responsável por abrir uma nova
conta bancária na aplicação, pertencente à camada de Aplicação
(Application Layer) da Clean Architecture.

Responsabilidades do caso de uso:
- Orquestrar repositórios e serviços externos (notificação)
- Validar pré-condições de regras do domínio (ex.: CPF duplicado)
- Criar entidades e aggregates utilizando suas factory methods
- Persistir o estado através dos repositórios
- Emitir notificações de evento (ex.: e-mail, SMS)

Importante:
Nenhuma regra de negócio deve ser escrita aqui.  
Regras pertencem ao domínio (entities, value objects, aggregates).
O caso de uso apenas coordena o fluxo.
"""

from ...domain.value_objects.cpf import CPF
from ...domain.aggregates.account import Account
from ...domain.exceptions import DuplicateCPFException

from ...domain.entities.customer import Customer
from ..ports.account_repository import IAccountRepository
from ..ports.customer_repository import ICustomerRepository
from ..ports.notification_service import INotificationService
from ..dto.open_account_dto import OpenAccountDTO


class OpenAccountUseCase:
    """
    Caso de uso para abertura de conta bancária.

    Ele coordena:
    - Verificação de CPF duplicado
    - Criação de Customer e Account
    - Persistência pelo repositório
    - Comunicação via serviço de notificação
    """

    def __init__(
        self,
        account_repo: IAccountRepository,
        customer_repo: ICustomerRepository,
        notifier: INotificationService
    ):
        """
        Inicializa o caso de uso com suas dependências externas.

        Parâmetros:
            account_repo: Repositório responsável por persistir Account
            customer_repo: Repositório responsável por obter/criar Customer
            notifier: Serviço de notificação (e-mail, SMS etc.)
        """
        self.account_repo = account_repo
        self.customer_repo = customer_repo
        self.notifier = notifier

    def execute(self, dto: OpenAccountDTO) -> Account:
        """
        Executa o fluxo de criação de uma nova conta.

        Etapas:
        1. Valida duplicidade de CPF
        2. Cria um Customer através do repositório
        3. Cria um Account usando seu factory method
        4. Persiste o aggregate no repositório
        5. Envia notificação ao cliente

        Retorna:
            Account: aggregate criado e persistido

        Raises:
            DuplicateCPFException: caso o CPF já esteja registrado
        """
        cpf = CPF(dto.cpf)

        # Verificação de duplicidade
        if self.customer_repo.get_by_cpf(cpf):
            raise DuplicateCPFException("Já existe uma conta com este CPF.")

        # Criação da entidade de domínio Customer
        customer = self.customer_repo.create(
            name=dto.name,
            email=dto.email,
            cpf=cpf,
            password_plain=dto.password,
        )

        # Criação do aggregate Account
        account = Account.open(customer)

        # Persistência
        self.account_repo.save(account)

        # Notificação
        self.notifier.notify(
            f"Conta {account.account_id[:8]} criada com sucesso para {customer.name}!"
        )

        return account
