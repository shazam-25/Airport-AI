# Verifies images & labels distribution

from pathlib import Path

images = list(Path("datasets/airport/images/train").glob(*.jpg))

labels = list(Path("datasets/airport/labels/train").glob(*.txt))

print("Images:", len(images))

print("Labels:", len(labels))