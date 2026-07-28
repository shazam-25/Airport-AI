from dataclasses import dataclass
from datetime import datetime

@dataclass
class SafetyEvent:
    """
    Represents one turnaround safety event.
    """
    timestamp: datetime
    camera_id: str
    track_id: int
    object_type: str
    event_type: str
    severity: str
    message: str

@dataclass
class SafetyZone:
    x1: float
    y1: float
    x2: float
    y2: float
    center_x: float
    center_y: float
    width: float
    height: float