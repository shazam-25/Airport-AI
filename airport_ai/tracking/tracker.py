from ultralytics import YOLO

class YOLOTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def track(self, frame):
        results = self.model.track(
            source=frame,
            persist=True,   # Keeps tracker state between consecutive frames
            tracker="bytetrack.yaml",
            conf=0.35,
            verbose=False
        )
        return results[0]