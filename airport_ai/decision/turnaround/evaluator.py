# from datetime import datetime
from typing import List
# from airport_ai.decision.turnaround.structures import SafetyEvent
# from airport_ai.decision.turnaround.zone import SafetyZoneGenerator
from airport_ai.inference.tracked_object import TrackedObject
from airport_ai.events.safety_event import SafetyEvent

from .zone import SafetyZone

class TurnaroundEvaluator:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.aircraft = None
        self.zone = None
    
    # def inside_zone(self, obj, zone):   # Point-In-Zone
    #     return (
    #         zone.x1 <= obj.center_x <= zone.x2
    #         and
    #         zone.y1 <= obj.center_y <= zone.y2
    #     )
    
    # def evaluate_person(self, obj): # Person Rule
    #     return SafetyEvent(
    #         timestamp=datetime.now(),
    #         camera_id=self.camera_id,
    #         track_id=obj.track_id,
    #         object_type=obj.class_name,
    #         event_type="Safety Zone Violation",
    #         severity="HIGH",
    #         message=f"Person {obj.track_id} entered aircraft safety zone."
    #     )
    
    # def evaluate_vehicle(self, obj): # Vehicle Rule
    #     return SafetyEvent(
    #         timestamp=datetime.now(),
    #         camera_id=self.camera_id,
    #         track_id=obj.track_id,
    #         object_type=obj.class_name,
    #         event_type="Vehicle Zone Violation",
    #         severity="MEDIUM",
    #         message=f"Vehicle {obj.track_id} entered aircraft safety zone."
    #     )
    
    # def evaluate_equipment(self, obj):  # Equipment rule
    #     return SafetyEvent(
    #         timestamp=datetime.now(),
    #         camera_id=self.camera_id,
    #         track_id=obj.track_id,
    #         object_type=obj.class_name,
    #         event_type="Equipment Zone Violation",
    #         severity="LOW",
    #         message=f"Equipment {obj.track_id} entered aircraft safety zone."
    #     )
    
    def evaluate(self, tracks: List[TrackedObject]):  # Main Evaluation Function
        events = []
        aircraft = self.select_aircraft(tracks)
        if aircraft:
            self.aircraft = aircraft
            self.zone = SafetyZone.from_aircraft(aircraft)
        if self.zone is None:
            return events
        assert self.aircraft is not None
        for obj in tracks:
            if obj.track_id == self.aircraft.track_id:
                continue
            if self.zone.contains(obj):
                events.append(
                    SafetyEvent(
                        camera_id=self.camera_id,
                        track_id=obj.track_id,
                        object_type=self.class_name(obj),
                        event_type="SAFETY_ZONE_INTRUSION",
                        severity="HIGH",
                        message=(
                            "Object inside aircraft "
                            "turnaround safety zone"
                        )
                    )
                )
        return events
    
    def select_aircraft(self, tracks):
        for obj in tracks:
            # update according to your YOLO class map
            if obj.class_id == 4:
                return obj
        return None
    
    def class_name(self,obj):
        return str(
            obj.class_id
        )