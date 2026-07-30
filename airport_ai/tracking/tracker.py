# from dataclasses import dataclass
from airport_ai.inference.tracked_object import TrackedObject
from typing import Dict

class ObjectTracker:
    def __init__(self, iou_threshold=0.5, max_missing_frames=30):
        # Active tracks indexed ID
        self.tracks: Dict[int, TrackedObject] = {}
        self.next_id = 1
        self.iou_threshold = iou_threshold  # MODIFICATION
        self.max_missing_frames = max_missing_frames
    
    def update(self, detections):
        results = []
        for detection in detections:
            track_id = self.assign_id(
                detection
            )
            if track_id is None:
                continue
            obj = TrackedObject.from_detection(
                track_id=track_id,
                detection=detection
            )
            self.tracks[track_id] = obj
            results.append(obj)
        return results

    def assign_id(self, detection):
        # Future tracking logic:
        # - IoU matching
        # - appearance embedding
        # - motion prediction
            track_id = self.next_id
            self.next_id += 1
            return track_id
            
    
    def calculate_iou(self, box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        intersection = max(0,x2-x1) * max(0,y2-y1)
        area1 = (
            (box1[2]-box1[0]) *
            (box1[3]-box1[1])
        )
        area2 = (
            (box2[2]-box2[0]) *
            (box2[3]-box2[1])
        )
        union = area1 + area2 - intersection
        if union == 0:
            return 0
        return intersection / union

    def predict_only(self):
        """
        ACalled when frames are skipped.
        maintains existing tracks.
        """
        predicted_tracks = []
        for track in self.tracks.values():
            track.mark_missed()
            if track.active:
                predicted_tracks.append(track)
        return predicted_tracks

    