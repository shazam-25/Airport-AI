from airport_ai.decision.ppe.structures import PPEStatus

class PPEAssociation:
    """
    Associates PPE detections with tracked person
    using bounding box overlap.
    """
    @staticmethod
    def iou(box_a, box_b):
        x_left = max(box_a.x1, box_b.x1)
        y_top = max(box_a.y1, box_b.y1)

        x_right = min(box_a.x2, box_b.x2)
        y_bottom = min(box_a.y2, box_b.y2)

        if x_right <= x_left or y_bottom <= y_top:
            return 0.0
        
        intersection = (x_right - x_left) * (y_bottom - y_top)

        area_a = box_a.width * box_a.height
        area_b = box_b.width * box_b.height

        union = area_a + area_b - intersection

        return intersection / union

    def __init__(self):
        self.vest_classes = {"safety_vest", "vest"}
        self.ear_classes = {"ear_protection", "earmuff"}
        self.threshold = 0.05

    def associate_person(self, person, tracked_objects): # Associate one person
        status = PPEStatus(person=person)
        for obj in tracked_objects:
            overlap = self.iou(person, obj)
            if overlap < self.threshold:
                continue
            name = obj.class_name.lower()
            if name in self.vest_classes:
                status.safety_vest = True
            elif name in self.ear_classes:
                status.ear_protection = True
        return status

    def associate(self, persons, tracked_objects):  # Associate all person
        statuses = []
        for person in persons:
            status = self.associate_person(person, tracked_objects)
            statuses.append(status)
        return statuses