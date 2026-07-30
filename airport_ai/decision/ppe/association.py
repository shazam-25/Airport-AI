# from airport_ai.config import config
from airport_ai.inference.tracked_object import TrackedObject
from .status import PPEStatus

class PPEAssociation:
    """
    Associates PPE detections with tracked person
    using bounding box overlap.
    """
    def __init__(self):
        self.vest_classes = {
            "safety_vest"
        }
        self.ear_classes = {
            "ear_protection"
        }
        self.threshold = 0.1

    # @staticmethod
    # def iou(box_a, box_b):
    #     x_left = max(box_a.x1, box_b.x1)
    #     y_top = max(box_a.y1, box_b.y1)

    #     x_right = min(box_a.x2, box_b.x2)
    #     y_bottom = min(box_a.y2, box_b.y2)

    #     if x_right <= x_left or y_bottom <= y_top:
    #         return 0.0
        
    #     intersection = (x_right - x_left) * (y_bottom - y_top)

    #     area_a = box_a.width * box_a.height
    #     area_b = box_b.width * box_b.height

    #     union = area_a + area_b - intersection

    #     return intersection / union

    # def __init__(self):
    #     self.vest_classes = {"safety_vest", "vest"}
    #     self.ear_classes = {"ear_protection", "earmuff"}
    #     self.threshold =  config.get("ppe")["association"]["overlap_threshold"]

    # def associate_person(self, person, tracked_objects): # Associate one person
    #     status = PPEStatus(person=person)
    #     for obj in tracked_objects:
    #         overlap = self.iou(person, obj)
    #         if overlap < self.threshold:
    #             continue
    #         name = obj.class_name.lower()
    #         if name in self.vest_classes:
    #             status.safety_vest = True
    #         elif name in self.ear_classes:
    #             status.ear_protection = True
    #     return status

    def associate(self, workers, ppe_items):  # Associate all person
        statuses = []
        for worker in workers:
            has_vest  = False
            has_ear_protection = False
            for item in ppe_items:
                # First check object type
                object_type = item.object_type.lower()
                if not worker.overlaps(item, threshold=self.threshold):
                    continue
                if object_type in self.vest_classes:
                    has_vest = True
                elif object_type in self.ear_classes:
                    has_ear_protection = True
            statuses.append(
                PPEStatus(
                    track_id=worker.track_id,
                    person=worker,
                    safety_vest=has_vest,
                    ear_protection=has_ear_protection,
                )
            )
        return statuses