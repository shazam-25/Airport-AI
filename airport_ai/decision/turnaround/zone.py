# from airport_ai.config import config
from dataclasses import dataclass
# from airport_ai.decision.turnaround.structures import SafetyZone

@dataclass
class SafetyZone:
    """
    Generates a configurable safety zone
    around the selected aircraft.
    """
    x1: float
    y1: float
    x2: float
    y2: float
    
    @classmethod
    def from_aircraft(
        cls,
        aircraft,
        margin=100
    ):
        return cls(
            x1=aircraft.x1 - margin,
            y1=aircraft.y1 - margin,
            x2=aircraft.x2 + margin,
            y2=aircraft.y2 + margin
        )
    
    def contains(
        self,
        obj
    ):
        cx, cy = obj.center
        return (
            self.x1 <= cx <= self.x2
            and
            self.y1 <= cy <= self.y2
        )

    # def __init__(self):
    #     turnaround_config = config.get("turnaround")
    #     zone_config = turnaround_config["safety_zone"]
    #     self.margin_x = zone_config["aircraft_margin_x"]
    #     self.margin_y = zone_config["aircraft)margin_y"]
    #     # self.margin_x = margin_x
    #     # self.margin_y = margin_y
    
    # def generate(self, aircraft):
    #     x1 = aircraft.x1 - self.margin_x
    #     y1 = aircraft.y1 - self.margin_y
    #     x2 = aircraft.x2 + self.margin_x
    #     y2 = aircraft.y2 + self.margin_y
    #     width = x2 - x1
    #     height = y2 - y1
    #     center_x = x1 + width / 2
    #     center_y = y1 + height / 2
    #     return SafetyZone(
    #         x1=x1,
    #         y1=y1,
    #         x2=x2,
    #         y2=y2,
    #         center_x=center_x,
    #         center_y=center_y,
    #         width=width,
    #         height=height
    #     )