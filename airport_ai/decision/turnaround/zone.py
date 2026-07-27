from airport_ai.decision.turnaround.structures import SafetyZone

class SafetyZoneGenerator:
    """
    Generates a configurable safety zone
    around the selected aircraft.
    """
    def __init__(self, margin_x, margin_y):
        self.margin_x = margin_x
        self.margin_y = margin_y
    
    def generate(self, aircraft):
        x1 = aircraft.x1 - self.margin_x
        y1 = aircraft.y1 - self.margin_y
        x2 = aircraft.x2 + self.margin_x
        y2 = aircraft.y2 + self.margin_y
        width = x2 - x1
        height = y2 - y1
        center_x = x1 + width / 2
        center_y = y1 + height / 2
        return SafetyZone(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            center_x=center_x,
            center_y=center_y,
            width=width,
            height=height
        )