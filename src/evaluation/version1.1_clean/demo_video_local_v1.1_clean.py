# src/evaluation/version1.1_clean/demo_video_local_v1.1_clean.py
"""
GhostDet v1.1_clean: Clean side-by-side demo (YOLO raw vs GhostDet stabilized).
- No text inside frames: only bboxes + confidence.
- Titles & jitter scores in top/bottom bars.
- Outputs 1280×252 MP4 (640×192 frames + 36px top + 30px bottom).
"""

import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from src.utils.video_utils import safe_plot, add_video_borders


def main():
    # ── Models ───────────────────────────────────────────────
    print(" Loading models...")
    yolo_model = YOLO("yolov8n.pt")  # Untuned baseline
    ghost_model = YOLO("runs/detect/ghostdet_local2/weights/best.pt")  # Fine-tuned

    # ── Data ─────────────────────────────────────────────────
    img_dir = Path("E:/KITTI/_temp_extract/img/training/image_02/0006")
    if not img_dir.exists():
        raise FileNotFoundError(f"KITTI seq-0006 not found at {img_dir}")

    # 50-frame demo (frames 100–149)
    frames = sorted(img_dir.glob("*.png"))[100:150]
    print(f" Rendering {len(frames)} frames (5 sec @ 10 FPS)")

    # ── Video Writer ─────────────────────────────────────────
    h, w = 192, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        "logs/ghostdet_clean_v1.1.mp4",
        fourcc, 10, (w * 2, h + 36 + 30)  # 1280 × 252
    )

    # ── Render Loop ──────────────────────────────────────────
    for i, frame_path in enumerate(frames):
        # Load & resize
        img = cv2.imread(str(frame_path))
        img_resized = cv2.resize(img, (w, h))

        # Inference
        yolo_res = yolo_model(img_resized, verbose=False)[0]
        ghost_res = ghost_model(img_resized, verbose=False)[0]

        # Clean plots (bbox + confidence only)
        yolo_plot = safe_plot(yolo_res)
        ghost_plot = safe_plot(ghost_res)

        # Status bar: frame count only (jitter requires history — see jitter_showcase_v1.1_clean.py)
        status = f"Frame {i + 1}/{len(frames)}"

        # Assemble
        canvas = add_video_borders(
            left_frame=yolo_plot,
            right_frame=ghost_plot,
            left_title="YOLOv8 (Untuned)",
            right_title="GhostDet (Fine-tuned)",
            status_text=status
        )

        out.write(canvas)
        if (i + 1) % 10 == 0:
            print(f"   Rendered {i + 1}/{len(frames)}")

    out.release()
    print(" Saved: logs/ghostdet_clean_v1.1.mp4")
    print(" Tip: Use jitter_showcase_v1.1_clean.py for real-time jitter scores.")


if __name__ == "__main__":
    main()