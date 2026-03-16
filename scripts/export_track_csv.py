from ultralytics import YOLO
import cv2
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = ROOT / "runs" / "detect" / "train1" / "weights" / "best.pt"
CONF = 0.25


def main():
    if len(sys.argv) < 3:
        raise RuntimeError("Usage: python export_track_csv.py <input_video> <output_csv>")

    video_path = sys.argv[1]
    out_csv = sys.argv[2]

    if not WEIGHTS.exists():
        raise FileNotFoundError(f"Model weights not found: {WEIGHTS}")

    model = YOLO(str(WEIGHTS))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)

    rows = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        res = model.predict(frame, conf=CONF, verbose=False)[0]

        best = None
        best_conf = -1.0

        if res.boxes is not None and len(res.boxes) > 0:
            for b in res.boxes:
                conf = float(b.conf[0].cpu().numpy())
                if conf > best_conf:
                    best_conf = conf
                    best = b

        if best is None:
            rows.append([frame_idx, frame_idx / fps, "", "", ""])
        else:
            x1, y1, x2, y2 = best.xyxy[0].cpu().numpy()
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            rows.append([frame_idx, frame_idx / fps, cx, cy, best_conf])

        frame_idx += 1

    cap.release()

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "time_s", "cx", "cy", "conf"])
        writer.writerows(rows)

    print(out_csv)


if __name__ == "__main__":
    main()