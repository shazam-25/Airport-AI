from ultralytics.data.annotator import auto_annotate
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

auto_annotate(
    data=PROJECT_ROOT/"datasets/airport/images/train",
    det_model="models/yolo11x.pt",
    sam_model="models/sam2_b.pt"
)

auto_annotate(
    data=PROJECT_ROOT/"datasets/airport/images/val",
    det_model="models/yolo11x.pt",
    sam_model="models/sam2_b.pt"
)

print("Finished")