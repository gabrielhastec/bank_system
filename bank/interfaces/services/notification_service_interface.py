"""Interface para serviços de notificações.

Define um contrato (protocolo) para operações de envio de notificações, como
e-mails, SMS ou push, permitindo que casos de uso dependam de uma abstração
em vez de implementações concretas.
"""

from typing import Protocol, runtime_checkable

@runtime_checkable
class NotificationServiceInterface(Protocol):
    """Contrato para serviços de notificações.

    Define métodos que implementações concretas devem seguir para enviar
    notificações (e.g., e-mail, SMS, push) no sistema.
    """
    
    def send_notification(self, recipient_id: int, title: str, body: str) -> bool:
        """Envia uma notificação para um destinatário.

        Args:
            recipient_id (int): Identificador do destinatário (ex.: user_id).
            title (str): Título ou resumo da notificação.
            body (str): Conteúdo ou descrição detalhada da notificação.

        Returns:
            bool: True se a notificação for enviada com sucesso, False caso contrário.
        """
        ...
