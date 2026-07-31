from pathlib import Path
import torch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
VIDEO_DIR = DATA_DIR / "videos"
IMAGE_DIR = DATA_DIR / "images"
OUTPUT_DIR = DATA_DIR / "output"
MODEL_PATH = PROJECT_ROOT / "models"
CONFIDENCE = 0.35
IMG_SIZE = 640
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

VIDEO_SOURCE = str(VIDEO_DIR / "01_sample.mp4")
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FRAME_QUEUE_SIZE = 10
FRAME_SKIP = 1

# Aircraft safety margin (pixels)
ZONE_MARGIN_X = 120
ZONE_MARGIN_Y = 80

# PPE requirements
REQUIRE_SAFETY_VEST = True
REQUIRE_EAR_PROTECTION = True

# FOD Rule
FOD_STATIONARY_SECONDS = 30

# Database
DATABASE_PATH = PROJECT_ROOT / "data/database/airport_monitor.db"

# Multi-Camera Support
CAMERAS = [
    {
        "camera_id": "GATE_A01",
        "name": "Gate A01",
        "source": str(VIDEO_DIR / "01_sample.mp4")
    },
    {
        "camera_id": "GATE_B03",
        "name": "Gate B03",
        "source": str(VIDEO_DIR/"02_sample.mp4")
    },
    {
        "camera_id": "GATE_C04",
        "name": "Gate C04",
        "source": str(VIDEO_DIR/"03_sample.mp4")
    }
]