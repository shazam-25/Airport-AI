from dataclasses import dataclass
from airport_ai.inference.tracked_object import TrackedObject

class ObjectTracker:
    def __init__(self):
        # Active tracks indexed ID
        self.tracks = {}
        self.next_id = 1
    
    def update(self, detections):
        tracked_objects = []
        for detection in detections:
            track_id = self.assign_id(detection)
            tracked_object = (TrackedObject.from_detection(track_id, detection))
            self.tracks[track_id] = tracked_object
            tracked_objects.append(tracked_object)
        return tracked_objects

    def assign_id(self, detection):
        # Future tracking logic:
        # - IoU matching
        # - appearance embedding
        # - motion prediction
        track_id = self.next_id
        self.next_id += 1
        return track_id

    def predict_only(self):
        """
        ACalled when frames are skipped.
        maintains existing tracks.
        """
        if not self.tracks:
            return []
        predicted_tracks = []
        for track_id, track in self.tracks.items():
            if hasattr(track, "predict"):
                track.predict()
            predicted_tracks.append(track)
        return predicted_tracks