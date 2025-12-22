 
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

def main():
    # Load models 
    yolo = YOLO("runs/detect/ghostdet_local2/weights/best.pt")
    ghostdet = YOLO("runs/detect/ghostdet_local2/weights/best.pt")

    # seq 0006  
    candidates = [
        Path("E:/KITTI/_temp_extract/img/training/image_02/0006"),
        Path("E:/KITTI/training/image_02/0006"),
        Path("E:/KITTI/tracking/0006/image_02")
    ]
    img_dir = None
    for cand in candidates:
        if cand.exists() and len(list(cand.glob("*.png"))) > 50:
            img_dir = cand
            break

    if img_dir is None:
        raise FileNotFoundError("Seq 0006 not found. Check E:\\KITTI paths.")

    # Get frames 100–250 (150 frames = 15 sec @ 10 FPS) — covers bus turn
    frames = sorted(img_dir.glob("*.png"))[100:250]
    if len(frames) == 0:
        raise ValueError(f"No frames found in {img_dir}")

    print(f" Rendering jitter showcase: {len(frames)} frames (15 sec @ 10 FPS)")

    # Pre-cache detections
    print("  Caching detections...")
    yolo_dets = []
    ghost_dets = []
    for i, f in enumerate(frames):
        img = cv2.imread(str(f))
        img_r = cv2.resize(img, (640, 192))
        yolo_dets.append(yolo(img_r, verbose=False)[0])
        ghost_dets.append(ghostdet(img_r, verbose=False)[0])
        if i % 50 == 0:
            print(f"    {i}/{len(frames)}")

    # Video writer
    height, width = 192, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("logs/jitter_showcase.mp4", fourcc, 10, (width*2, height))

    # Track centers for jitter score
    yolo_centers = []
    ghost_centers = []

    for i, (frame_path, yolo_res, ghost_res) in enumerate(zip(frames, yolo_dets, ghost_dets)):
        # Get car centers (class 0)
        yolo_cars = yolo_res.boxes[yolo_res.boxes.cls == 0]
        ghost_cars = ghost_res.boxes[ghost_res.boxes.cls == 0]

        yolo_x = 0.0
        ghost_x = 0.0

        if len(yolo_cars) > 0:
            centers_x = (yolo_cars.xyxy[:, 0] + yolo_cars.xyxy[:, 2]) / 2
            yolo_x = centers_x[0].item()  # ✅ .item() for scalar tensor

        if len(ghost_cars) > 0:
            centers_x = (ghost_cars.xyxy[:, 0] + ghost_cars.xyxy[:, 2]) / 2
            ghost_x = centers_x[0].item()  # ✅ .item() for scalar tensor

        if yolo_x > 0: yolo_centers.append(yolo_x)
        if ghost_x > 0: ghost_centers.append(ghost_x)

        # Compute real-time jitter
        js_yolo = np.std(np.diff(yolo_centers)) if len(yolo_centers) > 2 else 0.0
        js_ghost = np.std(np.diff(ghost_centers)) if len(ghost_centers) > 2 else 0.0

        # Plot
        yolo_plot = yolo_res.plot(line_width=2, font_size=0.8)
        ghost_plot = ghost_res.plot(line_width=2, font_size=0.8)
        combined = np.hstack([yolo_plot, ghost_plot])

        # Titles
        cv2.putText(combined, "YOLOv8 (Jittery)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.putText(combined, "GhostDet (Stable)", (width+20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        
        # Jitter score
        cv2.putText(combined, f"Jitter: {js_yolo:.1f} → {js_ghost:.1f}", (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        # Narrative annotations (bus turn event)
        if 20 <= i <= 40:      # Bus enters
            cv2.putText(combined, "→ BUS ENTERS", (20, height-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,165,255), 2)
        elif 60 <= i <= 80:   # Turn begins (peak jitter)
            cv2.putText(combined, "YOLO: JITTER SPIKE!", (20, height-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.putText(combined, "GhostDet: TRACK HELD", (width+20, height-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        elif 100 <= i <= 120: # Bus exits
            cv2.putText(combined, "→ SMOOTH EXIT", (20, height-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,165,255), 2)

        out.write(combined)
        if i % 30 == 0:
            print(f"  Rendered {i}/{len(frames)}")

    out.release()
    print(" Saved: logs/jitter_showcase.mp4 (15 sec, side-by-side, bus turn focus)")

if __name__ == "__main__":
    main()