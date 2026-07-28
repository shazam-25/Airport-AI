from airport_ai.alerts.models import Alert, AlertStatus
from airport_ai.alerts.priority import AlertPriority

class AlertManager:
    def __init__(self, repository, notifier):
        self.repository = repository
        self.notifier = notifier

    def creat_alert(self, stream: str, event):
        alert = Alert(
            alert_id=None,
            timestamp=event.timestamp,
            camera_id=event.camera_id,
            stream=stream,
            track_id=event.track_id,
            object_type=event.object_type,
            event_type=event.event_type,
            severity=event.severity,
            priority=AlertPriority.from_severity(event.severity),
            message=event.message,
            status=AlertStatus.NEW
        )
        self.repository.save(alert)
        self.notifier.notify(alert)