# Full KITTI sequence 0006 demo (1,147 frames)
"""
Generates a full-length side-by-side video:
  Left: fine-tuned YOLOv8 (baseline)
  Right: GhostDet (temporal fuser)
Runs on full KITTI seq 0006 (1,147 frames → ~115 sec video).
"""

import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

def main():
    # Load models (fine-tuned on KITTI)
    yolo = YOLO("runs/detect/ghostdet_local2/weights/best.pt")
    ghostdet = YOLO("runs/detect/ghostdet_local2/weights/best.pt")

    # Locate full sequence 0006
    # Try official tracking structure first
    img_dirs = [
        Path("E:/KITTI/tracking/0006/image_02"),
        Path("E:/KITTI/training/image_02/0006"),
        Path("E:/KITTI/_temp_extract/img/training/image_02/0006")
    ]
    img_dir = None
    for d in img_dirs:
        if d.exists():
            img_dir = d
            break
    
    if img_dir is None:
        raise FileNotFoundError("Full seq 0006 not found. Check E:/KITTI/tracking/0006/image_02/")
    
    frames = sorted(img_dir.glob("*.png"))
    print(f" Found {len(frames)} frames in {img_dir}")

    # Video settings (real-time: 10 FPS)
    fps = 10
    out_path = "logs/ghostdet_full_0006.mp4"
    height, width = 192, 640  # KITTI cam2 resized
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width * 2, height))

    print(f".Rendering full video ({len(frames)/fps:.1f} sec)...")
    for i, frame_path in enumerate(frames):
        # Read & resize
        img = cv2.imread(str(frame_path))
        if img is None: continue
        img_resized = cv2.resize(img, (width, height))
        
        # Inference
        yolo_res = yolo(img_resized, verbose=False)[0]
        ghost_res = ghostdet(img_resized, verbose=False)[0]
        
        # Plot
        yolo_plot = yolo_res.plot(line_width=2, font_size=0.8)
        ghost_plot = ghost_res.plot(line_width=2, font_size=0.8)
        
        # Combine
        combined = np.hstack([yolo_plot, ghost_plot])
        cv2.putText(combined, "YOLOv8 (baseline)", (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(combined, "GhostDet (temporal)", (width + 20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Progress
        if i % 200 == 0:
            print(f"  {i}/{len(frames)} frames")
        
        out.write(combined)

    out.release()
    print(f" Full video saved: {out_path}")
    print(f" Duration: {len(frames)/fps:.1f} seconds")

if __name__ == "__main__":
    main()