from typing import List
from airport_ai.tracking.structures import TrackedObject

class PersonSelector:
    """
    Selects tracked persons for PPE evaluation.
    """
    def select(
        self,
        tracked_objects: List[TrackedObject]
    ) -> List[TrackedObject]:
        return [
            obj for obj in tracked_objects if obj.class_name.lower() == "person"
        ]