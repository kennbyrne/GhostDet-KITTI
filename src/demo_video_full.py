# demo_video_full.py
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

def main():
    # Load models
    print(" Loading models...")
    yolo = YOLO("weights/yolov8n.pt")          
    ghostdet = YOLO("runs/detect/ghostdet_local2/weights/best.pt")  

    # PATH
    img_dir = Path("E:/KITTI/tracking/0006/image_02/0006")
    
    if not img_dir.exists():
        #fallback
        candidates = [
            Path("E:/KITTI/training/image_02/0006"),
            Path("E:/KITTI/_temp_extract/img/training/image_02/0006")
        ]
        for cand in candidates:
            if cand.exists():
                img_dir = cand
                print(f"⚠️  Using fallback: {img_dir}")
                break
        else:
            raise FileNotFoundError(" seq 0006 not found. Expected: E:/KITTI/tracking/0006/image_02/0006")

    frames = sorted(img_dir.glob("*.png"))
    print(f" Using: {img_dir}")
    print(f"   Found {len(frames)} frames")

    if len(frames) == 0:
        raise ValueError("No images found. Check folder contents.")

    # Video settings
    fps = 10
    out_path = "logs/ghostdet_seq0006_demo.mp4"
    height, width = 192, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width * 2, height))

    print(f" Rendering {len(frames)/fps:.1f}-sec video...")
    for i, frame_path in enumerate(frames):
        img = cv2.imread(str(frame_path))
        if img is None:
            continue
        img_resized = cv2.resize(img, (width, height))
        
        yolo_res = yolo(img_resized, verbose=False)[0]
        ghost_res = ghostdet(img_resized, verbose=False)[0]
        
        yolo_plot = yolo_res.plot(line_width=2, font_size=0.8)
        ghost_plot = ghost_res.plot(line_width=2, font_size=0.8)
        combined = np.hstack([yolo_plot, ghost_plot])
        
        cv2.putText(combined, "YOLOv8n (Baseline)", (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(combined, "GhostDet (Fine-Tuned)", (width + 20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if i % 50 == 0:
            print(f"  {i}/{len(frames)}")
        out.write(combined)

    out.release()
    print(f" Saved: {out_path} ({len(frames)/fps:.1f} sec)")

if __name__ == "__main__":
    main()