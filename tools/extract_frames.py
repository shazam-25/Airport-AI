import cv2
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

VIDEOS_PATH = PROJECT_ROOT / "data/videos"

OUTPUT_PATH = PROJECT_ROOT / "datasets/airport/images/train"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

videos = [
    "01_sample.mp4",
    "02_sample.mp4",
    "03_sample.mp4",
    "04_sample.mp4",
    "05_sample.mp4",
]
total_frames = 0

for video_name in videos:
    video_path = VIDEOS_PATH / video_name
    if not video_path.exists():
        print(f"Skipping missing video: {video_path}")
        continue

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"Cannot open: {video_path}")
        continue

    video_count = 0
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        # Extracts every 5th frame
        if frame_id % 5 == 0:
            filename = (
                f"{video_path.stem}_"
                f"{video_count:06d}.jpg"
            )
            cv2.imwrite(
                str(OUTPUT_PATH / filename),
                frame
            )

            video_count += 1
            total_frames += 1
        frame_id += 1
    cap.release()
    print(f"{video_name}: {video_count} frames")
print(f"\nTotal extracted frames: {total_frames}")
    