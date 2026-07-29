from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class FODEvent:
    """
    Represents one FOD Detection event.
    """
    camera_id: str
    track_id: int
    event_type: str
    severity: str
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)