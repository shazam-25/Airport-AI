from typing import List

from airport_ai.tracking.structures import TrackedObject

class FODSelector:
    """
    Selects objects that may become FOD.
    """
    def __init__(self):
        self.ignore_classes = {
            "person",
            "aircraft",
            "car",
            "truck",
            "bus",
            "van"
        }
    
    def select(
        self,
        tracked_objects: List[TrackedObject]
    ) -> List[TrackedObject]:
        return [
            obj for obj in tracked_objects if obj.class_name.lower() not in self.ignore_classes
        ]