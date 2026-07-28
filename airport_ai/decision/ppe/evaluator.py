from datetime import datetime
from airport_ai.decision.ppe.structures import PPEEvent

class PPEEvaluator:
    def __init__(self, camera_id, require_safety_vest=True, require_ear_protection=True):
        self.camera_id = camera_id
        self.require_safety_vest = require_safety_vest
        self.require_ear_protection = require_ear_protection

    def check_safety_vest(self, status): # Safety Vest Rule
        if self.require_safety_vest and not status.safety_vest:
            return PPEEvent(
                timestamp=datetime.now(),
                camera_id=self.camera_id,
                track_id=status.person.track_id,
                object_type="person",
                event_type="Safety Vest Missing",
                severity="HIGH",
                message=f"Worker {status.person.track_id} is not wearing a safety vest."
            )
        return None

    def check_ear_protection(self, status): # Ear Protection Rule
        if self.require_ear_protection and not status.ear_protection:
            return PPEEvent(
                timestamp=datetime.now(),
                camera_id=self.camera_id,
                track_id=status.person.track_id,
                object_type="person",
                event_type="Ear Protection Missing",
                severity="MEDIUM",
                message=f"Worker {status.person.track_id} is not wearing ear protection."
            )
        return None

    def evaluate(self, statuses):
        events = []
        for status in statuses:
            vest_event = self.check_safety_vest(status)
            if vest_event is not None:
                events.append(vest_event)
            
            ear_event = self.check_ear_protection(status)
            if ear_event is not None:
                events.append(ear_event)
        return events
