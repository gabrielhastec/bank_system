
import pytest
from unittest.mock import Mock

from src.application.use_cases.open_account import OpenAccountUseCase
from src.application.dto.open_account_dto import OpenAccountDTO
from src.domain.exceptions import DuplicateCPFException
from src.domain.value_objects.cpf import CPF

def test_open_account_success():
    # Criar mocks
    mock_account_repo = Mock()
    mock_customer_repo = Mock()
    mock_notifier = Mock()
    
    # Configurar o mock do customer_repo para retornar None (CPF não existe)
    mock_customer_repo.get_by_cpf.return_value = None
    
    # Configurar o mock do customer_repo.create para retornar um customer mock
    mock_customer = Mock()
    mock_customer.name = "Test User"
    mock_customer.email = "test@email.com"
    mock_customer.cpf = CPF("12345678900")
    mock_customer._password = None
    mock_customer_repo.create.return_value = mock_customer
    
    # Criar o caso de uso com os mocks
    uc = OpenAccountUseCase(mock_account_repo, mock_customer_repo, mock_notifier)
    
    dto = OpenAccountDTO(
        name="Test User",
        email="test@email.com",
        cpf="12345678900",
        password="password123"
    )
    
    # Mock do account
    mock_account = Mock()
    mock_account.account_id = "account123"
    mock_account.customer = mock_customer
    # Mock do método open da classe Account (que é um classmethod)
    with patch('src.domain.aggregates.account.Account.open') as mock_open:
        mock_open.return_value = mock_account
        account = uc.execute(dto)
    
    # Verificar que o método get_by_cpf foi chamado
    mock_customer_repo.get_by_cpf.assert_called_once()
    # Verificar que o método create foi chamado
    mock_customer_repo.create.assert_called_once()
    # Verificar que o método save foi chamado
    mock_account_repo.save.assert_called_once_with(mock_account)
    # Verificar que o notifier foi chamado
    mock_notifier.notify.assert_called_once()
    
    assert account == mock_account

def test_open_account_duplicate_cpf():
    mock_account_repo = Mock()
    mock_customer_repo = Mock()
    mock_notifier = Mock()
    
    # Configurar o mock para retornar um customer (simulando que o CPF já existe)
    mock_customer = Mock()
    mock_customer_repo.get_by_cpf.return_value = mock_customer
    
    uc = OpenAccountUseCase(mock_account_repo, mock_customer_repo, mock_notifier)
    
    dto = OpenAccountDTO(
        name="Test User",
        email="test@email.com",
        cpf="12345678900",
        password="password123"
    )
    
    with pytest.raises(DuplicateCPFException):
        uc.execute(dto)
    
    mock_customer_repo.get_by_cpf.assert_called_once()
    mock_customer_repo.create.assert_not_called()
    mock_account_repo.save.assert_not_called()
    mock_notifier.notify.assert_not_called()
