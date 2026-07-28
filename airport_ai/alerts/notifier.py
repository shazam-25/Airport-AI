class NotificationService:
    def notify(self, alert):
        raise NotImplementedError

class ConsoleNotifier(NotificationService):
    def notify(self, alert):
        print(
            f"[{alert.priority}] "
            f"{alert.camera_id} "
            f"{alert.stream}: "
            f"{alert.message}"
        )