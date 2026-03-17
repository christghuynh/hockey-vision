import sys
import cv2
from ultralytics import YOLO
from pathlib import Path

# ---------- PATH SETUP ----------

ROOT = Path(__file__).resolve().parents[1]

WEIGHTS = ROOT / "runs" / "detect" / "train1" / "weights" / "best.pt"

CONF = 0.25


def main():

    if len(sys.argv) < 3:
        raise RuntimeError("Usage: python run_inference.py <input_video> <output_video>")

    video_path = sys.argv[1]
    out_video = sys.argv[2]

    if not WEIGHTS.exists():
        raise FileNotFoundError(f"Model weights not found at: {WEIGHTS}")

    print(f"[run_inference] Loading model: {WEIGHTS}")

    model = YOLO(str(WEIGHTS))

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    Path(out_video).parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(out_video, fourcc, fps, (w, h))

    frame_idx = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model.predict(frame, conf=CONF, verbose=False)[0]

        if results.boxes is not None and len(results.boxes) > 0:
            for b in results.boxes:

                x1, y1, x2, y2 = b.xyxy[0].cpu().numpy().astype(int)
                conf = float(b.conf[0].cpu().numpy())

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

                cv2.putText(
                    frame,
                    f"puck {conf:.2f}",
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 255),
                    2,
                )

        out.write(frame)

        frame_idx += 1

        if frame_idx % 60 == 0:
            print(f"[run_inference] Processed {frame_idx} frames")

    cap.release()
    out.release()

    print(f"[run_inference] Saved video: {out_video}")


if __name__ == "__main__":
    main()