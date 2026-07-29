from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Detection:
    """
    Raw YOLO detection result.
    Produced by: YOLOEngine
    Consumed by: ObjectTracker
    """
    class_id: int
    confidence: float
    bbox: List[float]

    @property
    def x1(self):
        return self.bbox[0]
    
    @property
    def y1(self):
        return self.bbox[1]

    @property
    def x2(self):
        return self.bbox[2]

    @property
    def y2(self):
        return self.bbox[3]

    @property
    def center(self) -> Tuple[float, float]:
        return (
            (self.x1 + self.x2) / 2,
            (self.y1 + self.y2) / 2
        )

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1