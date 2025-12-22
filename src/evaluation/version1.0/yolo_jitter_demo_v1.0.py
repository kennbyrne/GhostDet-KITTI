# yolo_jitter_demo.py — Robust version (finds 270-frame seq 006)
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

def main():
    # Load model
    yolo = YOLO("runs/detect/ghostdet_local2/weights/best.pt")

    #  Search ALL possible seq 0006 locations (your structure)
    candidates = [
        Path("E:/KITTI/_temp_extract/img/training/image_02/0006"),
        Path("E:/KITTI/training/image_02/0006"),
        Path("E:/KITTI/tracking/0006/image_02"),
        Path("E:/KITTI/data_object_image_2/training"),
        Path("C:/Users/Suzan/Documents/GhostDet-KITTI/data/kitti_yolo/images/val")
    ]

    img_dir = None
    for cand in candidates:
        if cand.exists():
            # Count PNGs
            pngs = list(cand.glob("*.png"))
            if len(pngs) > 0:
                img_dir = cand
                print(f"✅ Found {len(pngs)} frames in: {cand}")
                break

    if img_dir is None:
        # Fallback: scan entire E:\KITTI for 000000.png
        print(" Scanning E:\\KITTI for frames...")
        for png in Path("E:/KITTI").rglob("000000.png"):
            img_dir = png.parent
            print(f" Found via scan: {img_dir}")
            break

    if img_dir is None:
        raise FileNotFoundError("No seq 0006 frames found. Check E:\\KITTI structure.")

    # Get first 50 frames
    frames = sorted(img_dir.glob("*.png"))[:50]
    if len(frames) == 0:
        raise ValueError(f"Found folder but no PNGs in {img_dir}")

    print(f" Rendering YOLO jitter demo: {len(frames)} frames")

    # Video writer
    height, width = 192, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("logs/yolo_jitter_demo.mp4", fourcc, 10, (width, height))

    for i, frame_path in enumerate(frames):
        img = cv2.imread(str(frame_path))
        if img is None: 
            continue
        img_resized = cv2.resize(img, (width, height))
        results = yolo(img_resized, verbose=False)[0]
        plot = results.plot(line_width=2, font_size=0.8)
        
        # Add diagnostic text
        cv2.putText(plot, "YOLOv8 (Jitter Demo)", (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(plot, f"Frame: {frame_path.stem}", (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        out.write(plot)
        if i % 10 == 0:
            print(f"  {i}/{len(frames)}")

    out.release()
    print(" Saved: logs/yolo_jitter_demo.mp4")

if __name__ == "__main__":
    main()