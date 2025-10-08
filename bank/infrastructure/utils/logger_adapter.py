"""Adaptador de logger para a camada de infraestrutura.

Fornece uma interface padronizada para integração do logger do núcleo da aplicação
com os repositórios, permitindo o registro de mensagens em diferentes níveis de log.
"""

from bank.core.utils.logger import get_logger

class LoggerAdapter:
    """Adaptador para logs na camada de infraestrutura.

    Encapsula o logger do núcleo da aplicação, fornecendo métodos simplificados
    para registro de mensagens em diferentes níveis (info, warning, error, debug).
    """
    def __init__(self, name: str):
        """Inicializa o adaptador com um logger configurado.

        Args:
            name (str): Nome do logger, geralmente o nome do módulo ou componente.
        """
        self.logger = get_logger(name)

    def info(self, message: str) -> None:
        """Registra uma mensagem no nível INFO.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Registra uma mensagem no nível WARNING.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Registra uma mensagem no nível ERROR.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Registra uma mensagem no nível DEBUG.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.debug(message)
