from dataclasses import dataclass
# from datetime import datetime
# from airport_ai.tracking.structures import TrackedObject

# @dataclass
# class PPEEvent:
#     """
#     Represents one PPE compliance event.
#     """
#     timestamp: datetime
#     camera_id: str
#     track_id: int
#     object_type: str
#     event_type: str
#     severity: str
#     message: str

@dataclass
class PPEStatus:
    """
    Stores PPE information for one tracked person.
    """
    track_id: int
    person: str
    safety_vest: bool = False
    ear_protection: bool = False