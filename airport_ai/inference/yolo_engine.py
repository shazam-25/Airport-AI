from ultralytics import YOLO
import torch
from airport_ai.inference.detection import Detection
from airport_ai.config import config

class YOLOEngine:
    def __init__(
        self,
        model_path,
        confidence=0.35,
        device="auto",
        image_size=640,
        half_precision=True,
        warmup=True,
        # batch_size=1,
    ):
        self.confidence = confidence
        self.image_size = config.get("model")["image_size"]
        # self.batch_size = batch_size
        self.iou = config.get("model")["iou"]   # MODIFICATION
        self.device = device

              
        # ===================
        # Device Selection
        # ===================
        self.device = self.select_device(device)

        # =================
        # Load Model
        # =================
        self.model = YOLO(model_path)  # MODIFICATION
        # Automatically load class names from the model -- MODIFICATION
        self.class_names = self.model.names

        # ================
        # FP16
        # ================
        self.half = (
            half_precision and self.device.startswith("cuda")
        )

        # ==============
        # Warmup
        # ==============
        if warmup:
            self.warmup()

        print(f"Loaded model: {model_path}")
        print(f"Device: {self.device}")
        print(f"Classes: {self.class_names}")

    def select_device(self, device):
        if device != "auto":
            return device
        
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def warmup(self):
        dummy = torch.zeros(
            (
                1,
                3,
                self.image_size,
                self.image_size
            ), device=self.device
        )
        dummy = dummy.to(self.device)

        self.model.predict(
                dummy, 
                imgsz=self.image_size, 
                conf=self.confidence,   # MODIFICATION
                iou=self.iou, # MODIFICATION
                device=self.device,
                half=self.half,
                verbose=False
        )
            

    def detect(self, frame):
        results = self.model.predict(
            source=frame,
            imgsz=self.image_size,
            conf=self.confidence,
            device=self.device,
            half=self.half,
            verbose=False
        )
        return self.parse_results(results)

    def parse_results(self, results):
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls.cpu().item())
                detection = Detection(
                            class_id=class_id,
                            class_name=self.class_names[class_id],  #MODIFICATION
                            confidence=float(box.conf.cpu().item()),
                            bbox=box.xyxy[0].cpu().tolist()
                        )
                detection.validate()
                detections.append(detection)
        return detections

    
