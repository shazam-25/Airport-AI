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
                    "time": now
                }
                continue
            elapsed = (now - previous["time"])
            if elapsed > self.stationary_threshold:
                events.append(
                    FODEvent(
                        camera_id=self.camera_id,
                        track_id=obj.track_id,
                        event_type="STATIONARY_FOD",
                        severity="MEDIUM",
                        message="{obj.track_id} FOD Detected",
                        timestamp=datetime.utcnow(),
                    )
                )
        return events
    
    # CHANGE LATER keep classes according to YOLO classes
    def is_fod_candidate(self, obj):
        return obj.class_id in [
            2,
            3,
            5
        ]