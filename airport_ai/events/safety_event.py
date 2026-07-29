from dataclasses import dataclass

@dataclass
class SafetyEvent:
    camera_id: str
    track_id: int
    object_type: str
    event_type: str
    severity: str
    message: str