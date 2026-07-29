# from datetime import datetime
from typing import List

from airport_ai.inference.tracked_object import TrackedObject
from airport_ai.events.ppe_event import PPEEvent

from .association import PPEAssociation
from datetime import datetime

class PPEEvaluator:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.association = PPEAssociation()
        self.rules = {
            "safety_vest_required": True,
            "ear_protection_required": True
        }

    # def check_safety_vest(self, status): # Safety Vest Rule
    #     if self.require_safety_vest and not status.safety_vest:
    #         return PPEEvent(
    #             timestamp=datetime.now(),
    #             camera_id=self.camera_id,
    #             track_id=status.person.track_id,
    #             object_type="person",
    #             event_type="Safety Vest Missing",
    #             severity="HIGH",
    #             message=f"Worker {status.person.track_id} is not wearing a safety vest."
    #         )
    #     return None

    # def check_ear_protection(self, status): # Ear Protection Rule
    #     if self.require_ear_protection and not status.ear_protection:
    #         return PPEEvent(
    #             timestamp=datetime.now(),
    #             camera_id=self.camera_id,
    #             track_id=status.person.track_id,
    #             object_type="person",
    #             event_type="Ear Protection Missing",
    #             severity="MEDIUM",
    #             message=f"Worker {status.person.track_id} is not wearing ear protection."
    #         )
    #     return None

    def evaluate(self, tracks: List[TrackedObject]):
        events = []
        person = [obj for obj in tracks if self.is_person(obj)]
        ppe_items = [obj for obj in tracks if self.is_ppe(obj)]
        statuses = self.association.associate(person, ppe_items)
        for status in statuses:
            if (self.rules["safety_vest_required"] and not status.safety_vest):
                events.append(
                    PPEEvent(
                        camera_id=self.camera_id,
                        track_id=status.track_id,
                        event_type="MISSING_SAFETY_VEST",
                        severity="MEDIUM",
                        message=f"Worker {status.person.track_id} is not wearing safety vest.",
                        timestamp=datetime.utcnow(),
                    )
                )
            if (self.rules["ear_protection_required"] and not status.ear_protection):
                events.append(
                    PPEEvent(
                        camera_id=self.camera_id,
                        track_id=status.track_id,
                        event_type="MISSING_EAR_PROTECTION",
                        severity="MEDIUM",
                        message=f"Worker {status.person.track_id} is not wearing ear protection.",
                        timestamp=datetime.utcnow(),
                    )
                )
        return events

    # CHANGE LATER according to YOLO classes (person class id)
    def is_person(self, obj):
        return obj.class_id == 13

    # CHANGE LATER according to YOLO classes (vest & ear class id)
    def is_ppe(self, obj):
        return obj.class_id in [14, 15]
