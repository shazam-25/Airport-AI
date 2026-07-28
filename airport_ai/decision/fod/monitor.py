import math
import time

from airport_ai.config import config
from airport_ai.decision.fod.structures import FODStatus

class StationaryMonitor:
    """
    Tracks stationary time for candidate objects.
    """
    def __init__(self):
        self.movement_threshold = config.get("fod")["movement_threshold"]
        self.history = {}

    def update(self, obj):
        now = time.time()
        if obj.track_id not in self.history:
            self.history[obj.track_id] = {
                "x": obj.center_x,
                "y": obj.center_y,
                "start_time": now,
            }

            return FODStatus(
                object=obj,
                stationary_seconds=0.0,
                is_stationary=False
            )
        
        previous = self.history[obj.track_id]

        distance = math.hypot(
            obj.center_x - previous["x"],
            obj.center_y - previous["y"]
        )

        if distance > self.movement_threshold:
            previous["x"] = obj.center_x
            previous["y"] = obj.center_y
            previous["start_time"] = now

            return FODStatus(
                object=obj,
                stationary_seconds = 0.0,
                is_stationary=False
            )
        
        stationary = now - previous["start_time"]

        return FODStatus(
            object=obj,
            stationary_seconds=stationary,
            is_stationary=True
        )