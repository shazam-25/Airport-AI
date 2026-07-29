from dataclasses import dataclass

@dataclass
class FODEvent:
    """
    Represents one FOD Detection event.
    """
    camera_id: str
    track_id: int
    event_type: str
    severity: str