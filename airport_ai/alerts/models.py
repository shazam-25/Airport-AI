from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class AlertStatus(Enum):
    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"

@dataclass
class Alert:
    alert_id: int | None
    timestamp: datetime
    camera_id: str
    stream: str
    track_id: int
    object_type: str
    event_type: str
    severity: str
    priority: str
    message: str
    status: AlertStatus