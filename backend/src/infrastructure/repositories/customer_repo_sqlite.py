"""
Repositório SQLite: CustomerRepositorySQLite
--------------------------------------------

Implementação concreta da porta (interface) ICustomerRepository,
localizada na camada de Infraestrutura da Clean Architecture.

Responsabilidades:
- Acessar o banco SQLite utilizando SQLModel
- Consultar e reconstruir entidades do domínio (Customer)
- Criar clientes em memória (pois a persistência efetiva ocorre
  através do AccountRepository, que é o ponto único de criação de contas)

Importante:
Este repositório **não** contém regras de negócio e não cria modelos
de domínio por conta própria — apenas traduz dados entre a persistência
e as entidades do domínio.
"""

from sqlmodel import Session, select

from ...application.ports.customer_repository import ICustomerRepository
from ...domain.entities.customer import Customer
from ...domain.value_objects.cpf import CPF
from ...domain.value_objects.password import Password
from ..database.orm import engine
from ..database.models.account_model import AccountModel


class CustomerRepositorySQLite(ICustomerRepository):
    """
    Implementação SQLite da interface ICustomerRepository.

    Este repositório é responsável por buscar e reconstruir a entidade
    Customer a partir dos dados armazenados no banco SQLite.
    """

    def create(self, name: str, email: str, cpf: CPF, password_plain: str) -> Customer:
        """
        Cria e retorna uma instância de Customer em memória.

        Nota:
        --------
        A persistência do cliente ocorre indiretamente através do
        AccountRepository. Portanto, este método apenas cria o objeto
        de domínio sem salvar diretamente no banco.
        """
        password = Password.create(password_plain) if password_plain else None

        return Customer(
            name=name,
            email=email,
            cpf=cpf,
            _password=password
        )

    def get_by_cpf(self, cpf: CPF) -> Customer | None:
        """
        Recupera um cliente persistido buscando pelo CPF.

        A consulta é feita na tabela de contas (AccountModel), que contém
        os dados do cliente associados à conta. Caso nenhum registro seja
        encontrado, retorna None.

        Retorna:
            Customer | None
        """
        with Session(engine) as session:
            stmt = select(AccountModel).where(
                AccountModel.customer_cpf == str(cpf)
            )
            result = session.exec(stmt).first()

            if not result:
                return None

            # Reconstrói entidade Customer a partir do modelo persistido
            password = (
                Password(hashed=result.password_hash)
                if result.password_hash
                else None
            )

            return Customer(
                name=result.customer_name,
                email=result.customer_email,
                cpf=CPF(result.customer_cpf),
                _password=password
            )
