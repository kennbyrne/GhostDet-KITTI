import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path

# Auto-detect run
runs_dir = Path("runs/detect")
if not runs_dir.exists():
    runs_dir = Path("runs/train")  # fallback

runs = [d for d in runs_dir.iterdir() if d.is_dir()]
if not runs:
    raise FileNotFoundError("No training runs found in runs/detect/ or runs/train/")

# latest run by modification time
latest_run = max(runs, key=lambda d: d.stat().st_mtime)
best_pt = latest_run / "weights" / "best.pt"

if not best_pt.exists():
    raise FileNotFoundError(f"best.pt not found in {best_pt.parent}")

print(f" Loading model from: {best_pt}")

# Load models
yolo_baseline = YOLO("yolov8n.pt")
ghostdet = YOLO(str(best_pt))

# Seq 0006 frames
frames = sorted([f for f in Path("E:/KITTI/_temp_extract/img/training/image_02/0006").glob("*.png")][100:150])  # 50-frame demo

# Video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("logs/ghostdet_vs_yolov8_local.mp4", fourcc, 10, (1280, 384))

for i, frame_path in enumerate(frames):
    img = cv2.imread(str(frame_path))
    img_resized = cv2.resize(img, (640, 192))
    
    # Inference
    yolo_res = yolo_baseline(img_resized, verbose=False)[0]
    ghost_res = ghostdet(img_resized, verbose=False)[0]
    
    # Plot
    yolo_plot = yolo_res.plot()
    ghost_plot = ghost_res.plot()
    
    # Concatenate
    combined = np.hstack([yolo_plot, ghost_plot])
    # Add labels
    cv2.putText(combined, "YOLOv8 (jittery)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
    cv2.putText(combined, "GhostDet (smooth)", (660, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    
    out.write(cv2.resize(combined, (1280, 384)))

out.release()
print(" Demo video saved to logs/ghostdet_vs_yolov8_local.mp4")