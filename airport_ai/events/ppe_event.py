from dataclasses import dataclass

@dataclass
class PPEEvent:
    camera_id: str
    track_id: int
    event_type: str
    severity: str