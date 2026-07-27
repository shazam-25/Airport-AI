from typing import List, Optional
from airport_ai.tracking.structures import TrackedObject

class AircraftSelector:
    """
    Selects the aircraft that will be used as the
    turnaorund safety reference.
    """
    def __init__(self):
        self.aircraft_classes = {
            "airplane",
            "aircraft",
            "plane"
        }

    def select(
        self,
        tracked_objects: List[TrackedObject]
    ) -> Optional[TrackedObject]:
        aircraft = [obj for obj in tracked_objects if obj.class_name.lower() in self.aircraft_classes]
        if not aircraft:
            return None
        return aircraft[0]