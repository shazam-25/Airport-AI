from datetime import datetime
from airport_ai.decision.turnaround.structures import SafetyEvent

class TurnaroundEvaluator:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.person_classes = {"person"}
        self.vehicle_classes = {"truck", "bus", "fuel_truck", "pushback_tug", "catering_truck", "baggage_cart"}
        self.equipment_classes = {"cone", "ladder", "toolbox", "container"}
    
    def inside_zone(self, obj, zone):   # Point-In-Zone
        return (
            zone.x1 <= obj.center_x <= zone.x2
            and
            zone.y1 <= obj.center_y <= zone.y2
        )
    
    def evaluate_person(self, obj): # Person Rule
        return SafetyEvent(
            timestamp=datetime.now(),
            camera_id=self.camera_id,
            track_id=obj.track_id,
            object_type=obj.class_name,
            event_type="Safety Zone Violation",
            severity="HIGH",
            message=f"Person {obj.track_id} entered aircraft safety zone."
        )
    
    def evaluate_vehicle(self, obj): # Vehicle Rule
        return SafetyEvent(
            timestamp=datetime.now(),
            camera_id=self.camera_id,
            track_id=obj.track_id,
            object_type=obj.class_name,
            event_type="Vehicle Zone Violation",
            severity="MEDIUM",
            message=f"Vehicle {obj.track_id} entered aircraft safety zone."
        )
    
    def evaluate_equipment(self, obj):  # Equipment rule
        return SafetyEvent(
            timestamp=datetime.now(),
            camera_id=self.camera_id,
            track_id=obj.track_id,
            object_type=obj.class_name,
            event_type="Equipment Zone Violation",
            severity="LOW",
            message=f"Equipment {obj.track_id} entered aircraft safety zone."
        )
    
    def evaluate(self, tracked_objects, zone):  # Main Evaluation Function
        events = []
        for obj in tracked_objects:
            if not self.inside_zone(obj, zone):
                continue
            if obj.class_name in self.person_classes:
                events.append(self.evaluate_person(obj))
            elif obj.class_name in self.vehicle_classes:
                events.append(self.evaluate_vehicle(obj))
            elif obj.class_name in self.equipment_classes:
                events.append(self.evaluate_equipment(obj))
        return events