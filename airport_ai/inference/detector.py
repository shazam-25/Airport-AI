from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, frame):
        results = self.model.predict(
            frame,
            verbose=False,
            conf=0.35
        )
        return results[0]