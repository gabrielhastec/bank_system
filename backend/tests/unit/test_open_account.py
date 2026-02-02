"""
Testes para o caso de uso OpenAccountUseCase.
"""
import pytest
from unittest.mock import Mock, MagicMock
from backend.src.application.use_cases.open_account import OpenAccountUseCase
from backend.src.application.dto.open_account_dto import OpenAccountDTO
from backend.src.domain.exceptions import DuplicateCPFException
from backend.src.domain.value_objects.cpf import CPF

class TestOpenAccountUseCase:
    
    def test_open_account_success(self):
        """Testa abertura de conta com sucesso"""
        # Arrange
        mock_account_repo = Mock()
        mock_customer_repo = Mock()
        mock_notifier = Mock()
        
        # Configurar mocks
        mock_customer_repo.get_by_cpf.return_value = None
        mock_customer = Mock()
        mock_customer.name = "João Silva"
        mock_customer.email = "joao@email.com"
        mock_customer.cpf = CPF("12345678900")
        mock_customer_repo.create.return_value = mock_customer
        
        mock_account = Mock()
        mock_account.account_id = "acc-123"
        mock_account.customer = mock_customer
        
        # Mock do método estático Account.open
        with patch('domain.aggregates.account.Account.open') as mock_open:
            mock_open.return_value = mock_account
            
            use_case = OpenAccountUseCase(
                account_repo=mock_account_repo,
                customer_repo=mock_customer_repo,
                notifier=mock_notifier
            )
            
            dto = OpenAccountDTO(
                name="João Silva",
                email="joao@email.com",
                cpf="12345678900",
                password="senha123"
            )
            
            # Act
            result = use_case.execute(dto)
            
            # Assert
            assert result == mock_account
            mock_customer_repo.get_by_cpf.assert_called_once()
            mock_customer_repo.create.assert_called_once()
            mock_account_repo.save.assert_called_once_with(mock_account)
            mock_notifier.notify.assert_called_once()
    
    def test_open_account_duplicate_cpf(self):
        """Testa tentativa de abrir conta com CPF duplicado"""
        # Arrange
        mock_account_repo = Mock()
        mock_customer_repo = Mock()
        mock_notifier = Mock()
        
        # CPF já existe
        mock_customer_repo.get_by_cpf.return_value = Mock()
        
        use_case = OpenAccountUseCase(
            account_repo=mock_account_repo,
            customer_repo=mock_customer_repo,
            notifier=mock_notifier
        )
        
        dto = OpenAccountDTO(
            name="João Silva",
            email="joao@email.com",
            cpf="12345678900",
            password="senha123"
        )
        
        # Act & Assert
        with pytest.raises(DuplicateCPFException):
            use_case.execute(dto)
        
        mock_customer_repo.get_by_cpf.assert_called_once()
        mock_customer_repo.create.assert_not_called()
        mock_account_repo.save.assert_not_called()
        mock_notifier.notify.assert_not_called()
    
    def test_open_account_invalid_password(self):
        """Testa validação de senha muito curta"""
        # Arrange
        use_case = OpenAccountUseCase(Mock(), Mock(), Mock())
        
        # Act & Assert
        with pytest.raises(ValueError, match="Password must be at least 6 characters"):
            dto = OpenAccountDTO(
                name="João Silva",
                email="joao@email.com",
                cpf="12345678900",
                password="123"  # Senha muito curta
            )
