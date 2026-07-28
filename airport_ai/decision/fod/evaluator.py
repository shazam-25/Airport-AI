from datetime import datetime
from airport_ai.decision.fod.structures import FODEvent

class FODEvaluator:
    def __init__(self, camera_id, stationary_threshold):
        self.camera_id = camera_id
        self.stationary_threshold = stationary_threshold

    def evaluate(self, statuses):
        events = []
        for status in statuses:
            if status.stationary_seconds >= self.stationary_threshold:
                status.is_fod = True
                events.append(
                    FODEvent(
                        timestamp=datetime.now(),
                        camera_id=self.camera_id,
                        track_id=status.object.track_id,
                        object_type=status.object.class_name,
                        event_type="Foreign Object Debris",
                        severity="HIGH",
                        message=(
                            f"{status.object.class_name} "
                            f"(ID {status.object.track_id}) has remained "
                            f"stationary for "
                            f"{status.stationary_seconds:.1f} seconds"
                        )
                    )
                )