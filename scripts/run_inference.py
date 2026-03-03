from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

VIDEO_PATH = "data/raw_videos/session9.MOV"
WEIGHTS = "runs/detect/train1/weights/best.pt"
OUT_VIDEO = "outputs/session9_pred.mp4"

CONF = 0.25 

model = YOLO(WEIGHTS)

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

Path("outputs").mkdir(exist_ok=True)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(OUT_VIDEO, fourcc, fps, (w, h))

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # predict on the frame
    results = model.predict(frame, conf=CONF, verbose=False)[0]

    # draw boxes
    if results.boxes is not None and len(results.boxes) > 0:
        for b in results.boxes:
            x1, y1, x2, y2 = b.xyxy[0].cpu().numpy().astype(int)
            conf = float(b.conf[0].cpu().numpy())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.putText(frame, f"puck {conf:.2f}", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    out.write(frame)

    frame_idx += 1
    if frame_idx % 60 == 0:
        print(f"Processed {frame_idx} frames...")

cap.release()
out.release()
print(f"Saved: {OUT_VIDEO}")