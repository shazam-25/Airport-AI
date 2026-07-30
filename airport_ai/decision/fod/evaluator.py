from airport_ai.config import config
import time
from datetime import datetime
from typing import List
from airport_ai.events.fod_event import FODEvent
from airport_ai.inference.tracked_object import TrackedObject

class FODEvaluator:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.history = {}
        self.stationary_threshold = config.get("fod")["stationary_seconds"]
        self.fod_classes = {"cone"}

    def evaluate(self, tracks: List[TrackedObject]):
        events = []
        now = time.time()
        for obj in tracks:
            if not self.is_fod_candidate(obj):
                continue
            previous = self.history.get(obj.track_id)
            if previous is None:
                self.history[obj.track_id] = {
                    "center": obj.center,
                    "time": now,
                    "alerted": False
                }
                continue
            elapsed = (now - previous["time"])
            if elapsed > self.stationary_threshold and not previous["alerted"]:
                events.append(
                    FODEvent(
                        camera_id=self.camera_id,
                        track_id=obj.track_id,
                        object_type=obj.object_type,
                        event_type="STATIONARY_FOD",
                        severity="LOW",
                        message=(
                            f"{obj.object_type} "
                            f"{obj.track_id} "
                            "FOD detected"
                        ),
                        timestamp=datetime.utcnow(),
                    )
                )
                previous["alerted"] = True
        return events
    
    # CHANGE LATER keep classes according to YOLO classes -- CHANGED
    def is_fod_candidate(self, obj: TrackedObject):
        return (obj.object_type in self.fod_classes)