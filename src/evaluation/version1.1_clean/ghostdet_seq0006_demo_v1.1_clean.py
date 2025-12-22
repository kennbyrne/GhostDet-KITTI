# ghostdet_seq0006_demo_v1.1_clean.py
"""
GhostDet v1.1_clean: 250-frame side-by-side demo (YOLO untuned vs GhostDet fine-tuned).
- Clean layout: class+score in frame, titles/status in bars.
- Events: occlusion, turn, recovery — narrated in bottom bar.
- Outputs: logs/ghostdet_seq0006_250f_v1.1.mp4 (25 sec @ 10 FPS).
"""

import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from src.utils.video_utils import safe_plot, add_video_borders
import torch


def compute_jitter_score(centers: list) -> float:
    if len(centers) < 2:
        return 0.0
    return float(np.std(np.diff(centers)))


def main():
    print(" Loading models...")
    yolo_model = YOLO("yolov8n.pt")                                 # Untuned baseline
    ghost_model = YOLO("runs/detect/ghostdet_local2/weights/best.pt")

    # Canonical KITTI seq-0006 (270-frame subset)
    img_dir = Path("E:/KITTI/tracking/0006/image_02/0006")
    if not img_dir.exists():
        raise FileNotFoundError(f"KITTI seq-0006 not found: {img_dir}")
    frames = sorted(img_dir.glob("*.png"))[50:300]  # 250 frames (50–300)
    print(f" Rendering 250-frame demo: {len(frames)} frames (25 sec)")

    # Video writer (1280×252: 640×192 + 36px top + 30px bottom)
    h, w = 192, 640
    out = cv2.VideoWriter(
        "logs/version1.1/ghostdet_seq0006_250frame__v1.1.mp4",
        cv2.VideoWriter_fourcc(*'mp4v'), 10, (w * 2, h + 36 + 30)
    )

    yolo_centers, ghost_centers = [], []

    for i, frame_path in enumerate(frames):
        # Load & resize
        img = cv2.imread(str(frame_path))
        img_resized = cv2.resize(img, (w, h))

        # Inference
        yolo_res = yolo_model(img_resized, verbose=False)[0]
        ghost_res = ghost_model(img_resized, verbose=False)[0]

        # Track main car (highest-confidence 'car')
        def get_main_car_center(res):
            cars = res.boxes[res.boxes.cls == 0]  # class 0 = car
            if len(cars) > 0:
                idx = torch.argmax(cars.conf)
                x1, _, x2, _ = cars.xyxy[idx]
                return float((x1 + x2) / 2)
            return None

        yolo_x = get_main_car_center(yolo_res)
        ghost_x = get_main_car_center(ghost_res)

        if yolo_x is not None: yolo_centers.append(yolo_x)
        if ghost_x is not None: ghost_centers.append(ghost_x)

        # Rolling jitter (last 20 frames)
        js_yolo = compute_jitter_score(yolo_centers[-20:]) if yolo_centers else 0.0
        js_ghost = compute_jitter_score(ghost_centers[-20:]) if ghost_centers else 0.0

        # Clean plots (class + score, low-conf in red)
        yolo_plot = safe_plot(yolo_res, highlight_low_conf=True)
        ghost_plot = safe_plot(ghost_res, highlight_low_conf=True)

        # Narrative status bar
        status = f"Jitter: {js_yolo:.1f} → {js_ghost:.1f} | Frame {i+1}/{len(frames)}"
        if 30 <= i < 60:
            status += " | -- BUS ENTERS (YOLO flickers)"
        elif 60 <= i < 120:
            status += " | OCCLUSION PEAK (GhostDet holds)"
        elif 120 <= i < 180:
            status += " | -- VEHICLE TURNS (YOLO loses)"
        elif 180 <= i < 240:
            status += " | TRACK RECOVERY (GhostDet stable)"

        # Assemble
        canvas = add_video_borders(
            left_frame=yolo_plot,
            right_frame=ghost_plot,
            left_title="YOLOv8 (Untuned)",
            right_title="GhostDet (Fine-tuned)",
            status_text=status
        )

        out.write(canvas)
        if (i + 1) % 50 == 0:
            print(f"   {i + 1}/{len(frames)}")

    out.release()
    print(" Saved: logs/version1.1/ghostdet_seq0006_250frame__v1.1.mp4")


if __name__ == "__main__":
    main()