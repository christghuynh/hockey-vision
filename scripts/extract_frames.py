import cv2
from pathlib import Path

# raw data
VIDEO_DIR = Path("data/raw_videos")

# extracted images
OUT_DIR = Path("data/frames")

# target FPS for frame extraction
TARGET_FPS = 3  

def extract(video_path: Path):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"Could not open {video_path.name}")
        return

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps <= 0:
        video_fps = 30

    # how often frames are saved
    stride = max(int(round(video_fps / TARGET_FPS)), 1) 

    name = video_path.stem
    frame_idx = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % stride == 0:
            out_path = OUT_DIR / f"{name}_f{frame_idx:06d}.jpg"
            cv2.imwrite(str(out_path), frame)
            saved += 1

        frame_idx += 1

    cap.release()
    print(f"{video_path.name}: saved {saved} frames (stride={stride}, fps={video_fps:.1f})")

def main():
    videos = sorted(
        list(VIDEO_DIR.glob("*.MOV"))
    )

    if not videos:
        print("No videos found in data/raw_videos/")
        return

    for vp in videos:
        extract(vp)

    print(f"\nDone. Frames saved to: {OUT_DIR}")

if __name__ == "__main__":
    main()