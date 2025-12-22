# Convert KITTI tracking labels → YOLO triplets
# Input: E:\KITTI\data_tracking_label_2\training\label_02\0006.txt
# Output: data/kitti_yolo/ (images, labels, triplets_val.txt)
# External Safety Requirement - USB-safe: Processes 1 frame at a time (low RAM)
import os
import cv2
import numpy as np
from pathlib import Path

# Paths
IMG_DIR = Path("E:/KITTI/_temp_extract/img/training/image_02/0006")
LBL_DIR = Path("E:/KITTI/_temp_extract/lbl/training/label_02/0006")
OUT_ROOT = Path("data/kitti_yolo")
OUT_ROOT.mkdir(parents=True, exist_ok=True)

IMG_OUT = OUT_ROOT / "images/val"
LBL_OUT = OUT_ROOT / "labels/val"
IMG_OUT.mkdir(parents=True, exist_ok=True)
LBL_OUT.mkdir(parents=True, exist_ok=True)

# KITTI → YOLO class map
CLASS_MAP = {"Car": 0, "Van": 0, "Truck": 1, "Pedestrian": 2, "Cyclist": 3}

def kitti_to_yolo(line, orig_w=1242, orig_h=375):
    parts = line.strip().split()
    if len(parts) < 15: return None
    cls = parts[0]
    if cls not in CLASS_MAP: return None
    try:
        x1, y1, x2, y2 = map(float, parts[4:8])
        x1, x2 = max(0, x1), min(orig_w, x2)
        y1, y2 = max(0, y1), min(orig_h, y2)
        if x2 <= x1 or y2 <= y1: return None
        xc = (x1 + x2) / 2 / orig_w
        yc = (y1 + y2) / 2 / orig_h
        w = (x2 - x1) / orig_w
        h = (y2 - y1) / orig_h
        return f"{CLASS_MAP[cls]} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}"
    except:
        return None

# Sorted frames
stems = sorted([f.stem for f in IMG_DIR.glob("*.png")])
print(f"Processing {len(stems)} frames...")

triplets = []
for i in range(1, len(stems) - 1):
    t0, t1, t2 = stems[i-1], stems[i], stems[i+1]
    
    # Process center frame
    img_path = IMG_DIR / f"{t1}.png"
    img = cv2.imread(str(img_path))
    resized = cv2.resize(img, (640, 192))
    cv2.imwrite(str(IMG_OUT / f"0006_{t1}.jpg"), resized)
    
    # Labels
    lbl_path = LBL_DIR / f"{t1}.txt"
    yolo_lines = []
    if lbl_path.exists():
        with open(lbl_path) as f:
            for line in f:
                yolo_line = kitti_to_yolo(line)
                if yolo_line:
                    yolo_lines.append(yolo_line)
    with open(LBL_OUT / f"0006_{t1}.txt", 'w') as f:
        f.write('\n'.join(yolo_lines))
    
    triplets.append(f"0006_{t0} 0006_{t1} 0006_{t2}")

# Save triplets & YAML
with open(OUT_ROOT / "triplets_val.txt", 'w') as f:
    f.write('\n'.join(triplets))

with open(OUT_ROOT / "kitti_ghostdet.yaml", 'w') as f:
    f.write("""path: ./data/kitti_yolo
val: images/val
nc: 4
names: ['car', 'truck', 'pedestrian', 'cyclist']
""")

print(f"Done. Triplets: {len(triplets)}")