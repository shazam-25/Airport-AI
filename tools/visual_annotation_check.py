# Verifies images load correctly.

from ultralytics import YOLO

model = YOLO("yolo26n.pt")

model.predict(
    "datasets/airport/images/train",
    save=True
)