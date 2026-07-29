from ultralytics import YOLO
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

model = YOLO("yolo26n.pt")

results = model.train(
    data=PROJECT_ROOT / "datasets/airport/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    device=0,
    patience=10,
    workers=4,
    fliplr=0.5, # Enable horizontal flip (50% probability)
    degrees= 10.0   # Enable rotation (+/- deg)
    scale=0.5   # Enable sacling
    project=PROJECT_ROOT / "models",
    name="airport_yolo"
)