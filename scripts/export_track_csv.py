from ultralytics import YOLO
import cv2
import csv
from pathlib import Path

VIDEO_PATH = "data/raw_videos/session9.MOV"
WEIGHTS = "runs/detect/train1/weights/best.pt"
OUT_CSV = "outputs/session9_track.csv"
CONF = 0.25

model = YOLO(WEIGHTS)

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS)
Path("outputs").mkdir(exist_ok=True)

rows = []
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    res = model.predict(frame, conf=CONF, verbose=False)[0]

    best = None
    best_conf = -1

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

with open(OUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["frame", "time_s", "cx", "cy", "conf"])
    writer.writerows(rows)

print(f"Saved: {OUT_CSV}")