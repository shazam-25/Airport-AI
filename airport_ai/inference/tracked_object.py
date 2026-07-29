from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import time

@dataclass
class TrackedObject:
    """
    Object after tracking.
    """
    track_id: int
    class_id: int
    confidence: float
    bbox: List[float]
    camera_id: Optional[str] = None
    timestamp: float = field(
        default_factory=time.time
    )
    age: int = 1
    missed_frames: int = 0
    active: bool = True

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
    def width(self):
        return self.x2 - self.x1


    @property
    def height(self):
        return self.y2 - self.y1


    @property
    def center(self) -> Tuple[float, float]:
        return (
            (self.x1 + self.x2) / 2,
            (self.y1 + self.y2) / 2
        )
    
    @property
    def area(self):
        return (
            self.width *
            self.height
        )

    def overlaps(
        self,
        other,
        threshold=0.5
    ):
        """
        Bounding box overlap test.

        Used by:
            PPE association
            FOD proximity checks
        """
        x_left = max(
            self.x1,
            other.x1
        )
        y_top = max(
            self.y1,
            other.y1
        )
        x_right = min(
            self.x2,
            other.x2
        )
        y_bottom = min(
            self.y2,
            other.y2
        )
        if (
            x_right <= x_left
            or y_bottom <= y_top
        ):
            return False

        intersection = (
            (x_right - x_left) *
            (y_bottom - y_top)
        )

        union = (
            self.area +
            other.area -
            intersection
        )

        iou = intersection / union
        return iou >= threshold


    def update_bbox(
        self,
        bbox
    ):
        """
        Update position during tracking.
        """
        self.bbox = bbox
        self.age += 1
        self.missed_frames = 0
        self.timestamp = time.time()

    def mark_missed(self):
        self.missed_frames += 1
        if self.missed_frames > 30:
            self.active = False

    def to_dict(self):
        return {
            "track_id": self.track_id,
            "class_id": self.class_id,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "camera_id": self.camera_id,
            "timestamp": self.timestamp,
            "age": self.age,
            "missed_frames": self.missed_frames,
            "active": self.active,
        }

    @classmethod
    def from_detection(
        cls,
        track_id,
        detection,
        camera_id=None
    ):
        """
        Convert YOLO Detection
        into tracked object.
        """
        return cls(
            track_id=track_id,
            class_id=detection.class_id,
            confidence=detection.confidence,
            bbox=detection.bbox,
            camera_id=camera_id
        )