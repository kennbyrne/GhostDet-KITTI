# generate_kitti_mot.py
from pathlib import Path
from ultralytics import YOLO

# Load fine-tuned GhostDet model
model = YOLO("runs/detect/ghostdet_local2/weights/best.pt")

# Output dir (TrackEval expects: data/trackers/kitti/kitti_train/ghostdet/data/)
out_dir = Path("tools/TrackEval/data/trackers/kitti/kitti_train/ghostdet/data")
out_dir.mkdir(parents=True, exist_ok=True)

# Generate predictions for seq-0006 (270 frames)
with open(out_dir / "0006.txt", "w") as f:
    for i, img_path in enumerate(sorted(Path("E:/KITTI/tracking/0006/image_02/0006").glob("*.png"))):
        frame_id = i + 1  # 1-based
        results = model(str(img_path), verbose=False)[0]
        for box in results.boxes:
            cls_id = int(box.cls)
            # Only cars (0=car, 1=van → map both to class 1 for KITTI MOT)
            if cls_id in [0, 1]:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf)
                # KITTI MOT format: <frame> <id> <x> <y> <w> <h> <score> <x3d> <y3d> <z3d>
                f.write(f"{frame_id} -1 {x1:.2f} {y1:.2f} {x2-x1:.2f} {y2-y1:.2f} {conf:.6f} -1 -1 -1\n")