# generate_mot_results.py
from pathlib import Path
from ultralytics import YOLO

model = YOLO("runs/detect/ghostdet_local2/weights/best.pt")
out_dir = Path("logs/ghostdet_mot")
out_dir.mkdir(parents=True, exist_ok=True)

# KITTI class map: car=1, pedestrian=2, cyclist=3 (MOT uses 1-based)
CLASS_MAP = {0: 1, 1: 1, 2: 2, 3: 3}  # van→car, truck→car

with open(out_dir / "0006.txt", "w") as f:
    for i, img_path in enumerate(sorted(Path("E:/KITTI/tracking/0006/image_02").glob("*.png"))):
        frame_id = i + 1  # KITTI MOT uses 1-based frame IDs
        results = model(img_path, verbose=False)[0]
        boxes = results.boxes
        for j, box in enumerate(boxes):
            cls_id = int(box.cls)
            if cls_id not in CLASS_MAP:
                continue
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf)
            # MOT format: <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
            f.write(f"{frame_id},-1,{x1:.2f},{y1:.2f},{x2-x1:.2f},{y2-y1:.2f},{conf:.3f},-1,-1,-1\n")