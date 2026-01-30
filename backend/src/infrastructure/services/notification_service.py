

from ...application.ports.notification_service import INotificationService

class ConsoleNotificationService(INotificationService):
    def notify(self, message: str) -> None:
        print(f"[NOTIFICAÇÃO] {message}")
        