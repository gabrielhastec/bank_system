"""
Container de Injeção de Dependências
------------------------------------

Este módulo configura o contêiner de IoC (Inversion of Control) usando
`dependency_injector`, responsável por montar e fornecer todas as
dependências da aplicação.

Camada: Config / Cross-cutting

Responsabilidades:
- Registrar implementações concretas de repositórios
- Registrar serviços externos (ex.: notificações)
- Construir instâncias de casos de uso com dependências automaticamente
- Servir como Composition Root da aplicação

Importante:
Não contém regras de negócio nem lógica de aplicação.
Apenas **liga** as partes da arquitetura.
"""

from dependency_injector import containers, providers

from ..application.use_cases.open_account import OpenAccountUseCase
from ..application.use_cases.login import LoginUseCase
from ..application.use_cases.make_deposit import MakeDepositUseCase
from ..application.use_cases.make_withdrawal import MakeWithdrawalUseCase
from ..application.use_cases.make_transfer import MakeTransferUseCase
from ..application.use_cases.get_statement import GetStatementUseCase
from ..infrastructure.repositories.account_repo_sqlite import AccountRepositorySQLite
from ..infrastructure.repositories.customer_repo_sqlite import CustomerRepositorySQLite
from ..infrastructure.services.notification_service import ConsoleNotificationService

class Container(containers.DeclarativeContainer):
    """
    Contêiner de injeção de dependências da aplicação.

    Cada provider abaixo representa um componente da arquitetura e
    define como ele será instanciado e compartilhado.
    """

    # Repositórios (Infraestrutura)
    account_repo = providers.Singleton(AccountRepositorySQLite)
    customer_repo = providers.Singleton(CustomerRepositorySQLite)

    # Serviços externos (Infraestrutura)
    notifier = providers.Singleton(ConsoleNotificationService)

    # Casos de uso (Aplicação)
    open_account_uc = providers.Factory(
        OpenAccountUseCase,
        account_repo=account_repo,
        customer_repo=customer_repo,
        notifier=notifier,
    )

    login_uc = providers.Factory(
        LoginUseCase,
        customer_repo=customer_repo,
        account_repo=account_repo,
    )

    deposit_uc = providers.Factory(
        MakeDepositUseCase,
        account_repo=account_repo,
    )

    withdrawal_uc = providers.Factory(
        MakeWithdrawalUseCase,
        account_repo=account_repo,
    )

    transfer_uc = providers.Factory(
        MakeTransferUseCase,
        account_repo=account_repo,
    )

    statement_uc = providers.Factory(
        GetStatementUseCase,
        account_repo=account_repo,
    )

# Instância global do contêiner
container = Container()

# Exposição de fábrica dos casos de uso
get_open_account_uc = container.open_account_uc
get_login_uc = container.login_uc
get_deposit_uc = container.deposit_uc
get_withdrawal_uc = container.withdrawal_uc
get_transfer_uc = container.transfer_uc
get_statement_uc = container.statement_uc
