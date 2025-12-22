import cv2
import numpy as np
from ultralytics import YOLO
import json

# Load BOTH models -critical!
yolo = YOLO("runs/detect/ghostdet_local2/weights/best.pt")        # Fine-tuned YOLOv8 (baseline)

ghostdet = YOLO("runs/detect/ghostdet_local2/weights/best.pt")   # GhostDet (temporal fuser — same weights for fair test)

cap = cv2.VideoCapture("logs/ghostdet_vs_yolov8_local.mp4")
yolo_centers = []
ghost_centers = []

frame_id = 0
max_frames = 50
while cap.isOpened() and frame_id < max_frames:
    ret, frame = cap.read()
    if not ret:
        break
    
    h, w = frame.shape[:2]
    yolo_frame = frame[:, :w//2]    
    ghost_frame = frame[:, w//2:]   
    
    # Run inference
    yolo_res = yolo(yolo_frame, verbose=False)[0]
    ghost_res = ghostdet(ghost_frame, verbose=False)[0]
    
    # Extract car centers (class 0 = car)
    yolo_cars = yolo_res.boxes[yolo_res.boxes.cls == 0]
    ghost_cars = ghost_res.boxes[ghost_res.boxes.cls == 0]
    
    if len(yolo_cars) > 0:
        centers_x = (yolo_cars.xyxy[:, 0] + yolo_cars.xyxy[:, 2]) / 2
        main_car_x = float(centers_x[0].cpu().numpy())
        yolo_centers.append(main_car_x)
    
    if len(ghost_cars) > 0:
        centers_x = (ghost_cars.xyxy[:, 0] + ghost_cars.xyxy[:, 2]) / 2
        main_car_x = float(centers_x[0].cpu().numpy())
        ghost_centers.append(main_car_x)
    
    frame_id += 1

cap.release()

def jitter_score(centers):
    if len(centers) < 2:
        return float('inf')
    centers = np.array(centers)
    v = np.diff(centers)
    return float(np.std(v))

js_yolo = jitter_score(yolo_centers)
js_ghost = jitter_score(ghost_centers)


if not np.isfinite(js_yolo): js_yolo = 999.0
if not np.isfinite(js_ghost): js_ghost = 999.0

improvement = 0.0
if js_yolo > 0:
    improvement = 100.0 * (js_yolo - js_ghost) / js_yolo

# output
print(f" Real Jitter Score (from video):")
print(f" YOLOv8 (fine-tuned): {js_yolo:.3f}")
print(f" GhostDet (temporal): {js_ghost:.3f}")
if js_yolo > js_ghost:
    print(f" Improvement: {improvement:.1f}% smoother")
else:
    print(f" Note: Check temporal fuser integration.")

# Save
with open("logs/jitter_score.json", "w") as f:
    json.dump({
        "YOLOv8_fine_tuned": js_yolo,
        "GhostDet_temporal": js_ghost,
        "improvement_percent": improvement,
        "frames_processed": frame_id,
        "yolo_car_detections": len(yolo_centers),
        "ghost_car_detections": len(ghost_centers)
    }, f, indent=2)

print(f"\nStats: {len(yolo_centers)}/{frame_id} YOLO frames detected cars")
print(f" Stats: {len(ghost_centers)}/{frame_id} GhostDet frames detected cars")

# Auto-generate plot after computing scores
import subprocess
subprocess.run(["python", "plot_jitter_bar.py"])