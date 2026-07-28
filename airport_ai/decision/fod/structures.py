from dataclasses import dataclass
from datetime import datetime

from airport_ai.tracking.structures import TrackedObject

@dataclass
class FODEvent:
    """
    Represents one FOD Detection event.
    """
    timestamp: datetime
    track_id: int
    object_type: str
    event_type: str
    severity: str
    message:str

@dataclass
class FODStatus:
    """
    Stores the monitoring state for a tracked object.
    """
    object: TrackedObject
    stationary_seconds: float
    is_stationary: bool
    is_fod: bool = False

