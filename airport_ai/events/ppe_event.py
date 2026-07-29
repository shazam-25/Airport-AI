from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PPEEvent:
    camera_id: str
    track_id: int
    event_type: str
    severity: str
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)