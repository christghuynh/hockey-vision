import cv2
import time

VIDEO_PATH = "data/raw_videos/session1.MOV"

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Could not open video.")
    exit()

video_fps = cap.get(cv2.CAP_PROP_FPS)
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Original Video FPS: {video_fps}")
print(f"Resolution: {video_width} x {video_height}")

# contours
frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # resize
    scale = 0.3
    h, w = frame.shape[:2]
    frame_resized = cv2.resize(frame, (int(w * scale), int(h * scale)))

    # fps calculation
    elapsed = time.time() - start_time
    processing_fps = frame_count / elapsed if elapsed > 0 else 0

    cv2.putText(frame_resized,
                f"Frame: {frame_count}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2)

    cv2.putText(frame_resized,
                f"Processing FPS: {processing_fps:.2f}",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2)

    cv2.imshow("Video", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

end_time = time.time()

print(f"\nTotal Frames Processed: {frame_count}")
print(f"Final Processing FPS: {frame_count / (end_time - start_time):.2f}")

cap.release()
cv2.destroyAllWindows()