from pathlib import Path
from posix import pathconf

PROJECT_ROOT = Path(__file__).resolve().parents[1]

LABEL_DIRS = [
    Path(PROJECT_ROOT / "datasets/airport/train/labels"),
    Path(PROJECT_ROOT / "datasets/airport/val/labels"),
    Path(PROJECT_ROOT / "datasets/airport/test/labels"),
]

for label_dir in LABEL_DIRS:
    for txt_file in label_dir.glob("*.txt"):
        output_lines = []
        with open(txt_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 7:
                    continue

                cls = parts[0]
                coords = list(map(float, parts[1:]))

                xs = coords[0::2]
                ys = coords[1::2]
                xmin = min(xs)
                xmax = max(xs)
                ymin = min(ys)
                ymax = max(ys)

                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2
                width = xmax - xmin
                height = ymax - ymin

                output_lines.append(
                    f"{cls} "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{width:.6f} "
                    f"{height:.6f}"
                )
        with open(txt_file, "w") as f:
            f.write("\n".join(output_lines))

print("✅ Converted segmentation labels to YOLO detection labels.")