from ultralytics import YOLO
from airport_ai.config import config

class ObjectTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def track(self, frame):
        tracking_config = config.get("tracking")
        results = self.model.track(
            source=frame,
            persist=True,   # Keeps tracker state between consecutive frames
            tracker=tracking_config["tracker"],
            conf=0.35,
            verbose=False
        )
        return results[0]