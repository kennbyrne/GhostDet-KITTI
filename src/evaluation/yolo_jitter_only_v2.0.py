# yolo_jitter_only.py — Pure YOLOv8n Jitter Failure Showcase (30 sec)
import cv2
import numpy as np
import os
from pathlib import Path

os.makedirs("logs", exist_ok=True)

try:
    from ultralytics import YOLO
except ImportError as e:
    print(" Missing:", e)
    exit(1)

def main():
    # 🔹 Load YOLOv8n (baseline — no blur augmentation)
    print(" Loading YOLOv8n...")
    model = YOLO("weights/yolov8n.pt")  # Ensure this file exists

    # 🔍 Find seq 0006 or fallback to seq 0000
    candidates = [
        Path("E:/KITTI/_temp_extract/img/training/image_02/0006"),
        Path("E:/KITTI/training/image_02/0006"),
        Path("E:/KITTI/tracking/0006/image_02"),
        Path("E:/KITTI/tracking/0000/image_02")
    ]
    img_dir = None
    for cand in candidates:
        if cand.exists() and len(list(cand.glob("*.png"))) > 200:
            img_dir = cand
            break

    if img_dir is None:
        raise FileNotFoundError("Seq 0000/0006 not found. Check E:\\KITTI.")

    #  Use frames 50–350 (300 frames = 30 sec @ 10 FPS)
    frames = sorted(img_dir.glob("*.png"))[50:350]
    print(f" Rendering 30-sec YOLO jitter showcase: {len(frames)} frames")

    # Pre-cache detections
    print("  Caching detections...")
    detections = []
    for i, f in enumerate(frames):
        img = cv2.imread(str(f))
        img_r = cv2.resize(img, (640, 192))
        detections.append(model(img_r, verbose=False)[0])
        if (i + 1) % 50 == 0:
            print(f"    {i+1}/{len(frames)}")

    # Video writer: 10 FPS, 640×192
    height, width = 192, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("logs/yolo_jitter_only.mp4", fourcc, 10, (width, height))

    # Track car centers (class 0 = 'car')
    centers = []
    jitter_scores = []

    for i, (frame_path, res) in enumerate(zip(frames, detections)):
        # Extract car bbox center x
        cars = res.boxes[res.boxes.cls == 0]
        x_center = 0.0

        if len(cars) > 0:
            x1, _, x2, _ = cars.xyxy[0]
            x_center = ((x1 + x2) / 2).item()

        if x_center > 0:
            centers.append(x_center)

        # Compute jitter (std of center velocity)
        jitter_score = float(np.std(np.diff(centers))) if len(centers) > 2 else 0.0
        jitter_scores.append(jitter_score)

        # Plot
        plot_img = res.plot(line_width=2, font_size=0.8)

        # Color overlay based on jitter
        if jitter_score > 2.0:  # High jitter → red tint
            overlay = np.zeros_like(plot_img)
            overlay[:, :, 2] = 50  # Red channel
            plot_img = cv2.addWeighted(plot_img, 0.7, overlay, 0.3, 0)
        elif jitter_score > 1.0:  # Medium jitter → yellow tint
            overlay = np.zeros_like(plot_img)
            overlay[:, :, 0] = 30  # Blue channel
            overlay[:, :, 2] = 30  # Red channel
            plot_img = cv2.addWeighted(plot_img, 0.7, overlay, 0.3, 0)

        # Titles & jitter score
        cv2.putText(plot_img, "YOLOv8n — JITTER FAILURE MODE", (20, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(plot_img, f"Jitter Score: {jitter_score:.1f}", (20, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        #  Dramatic narrative annotations
        if 40 <= i < 80:      # Bus appears
            cv2.putText(plot_img, "→ BUS ENTERS (OCCLUSION BEGINS)", (20, height - 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
        elif 80 <= i < 140:   # Peak jitter — YOLO fails
            cv2.putText(plot_img, "YOLO: BOX JUMPING!", (20, height - 55),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.putText(plot_img, "→ MAX OCCLUSION", (20, height - 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        elif 140 <= i < 220:  # Turn & motion blur
            cv2.putText(plot_img, "→ CAR TURNS (MOTION BLUR)", (20, height - 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        elif i >= 220:        # Recovery attempt
            if len(centers) > 10 and jitter_score < 1.0:
                cv2.putText(plot_img, "RECOVERY ATTEMPT", (20, height - 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        out.write(plot_img)
        if (i + 1) % 30 == 0:
            print(f"  Rendered {i+1}/{len(frames)}")

    out.release()
    print("Saved: logs/yolo_jitter_only.mp4 (30 sec, pure YOLO failure)")

if __name__ == "__main__":
    main()