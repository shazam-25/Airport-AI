from pathlib import Path
import random
import shutil

random.seed(42)

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

raw = PROJECT_ROOT / "datasets/airport/raw_frames"

images = sorted(raw.glob("*.jpg"))
# print(len(images))

random.shuffle(images)

split = int(len(images) * 0.8)

train = images[:split]
val = images[split:]

train_dir = PROJECT_ROOT / "datasets/airport/images/train"
val_dir = PROJECT_ROOT / "datasets/airport/images/val"

train_dir.mkdir(parents=True, exist_ok=True)
val_dir.mkdir(parents=True, exist_ok=True)

for img in train:
    shutil.copy(img, train_dir / img.name)

for img in val:
    shutil.copy(img, val_dir / img.name)

print(len(train), len(val))