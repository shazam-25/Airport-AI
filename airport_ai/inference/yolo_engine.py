from ultralytics import YOLO
import torch

class YOLOEngine:
    def __init__(
        self,
        model_path,
        confidence=0.35,
        device="auto",
        image_size=640,
        half_precision=True,
        warmup=True,
        batch_size=1,
    ):
        self.confidence = confidence
        self.image_size = image_size
        self.batch_size = batch_size

        # ===================
        # Device Selection
        # ===================
        self.device = self.select_device(device)

        # =================
        # Load Model
        # =================
        self.model = YOLO(model_path)

        # ================
        # FP16
        # ================
        self.half = (
            half_precision and self.device != "cpu"
        )

        # ==============
        # Warmup
        # ==============
        if warmup:
            self.warmup()

    def select_device(self, device):
        if device != "auto":
            return device
        
        if torch.cuda.is_available():
            return "cuda"

    
