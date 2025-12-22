"""
preprocess_kitti_local_v1.1_clean.py
Convert KITTI tracking labels → YOLO format + triplet list for GhostDet v1.1_clean.

Inputs:
  - Images: E:/KITTI/tracking/0006/image_02/0006/*.png
  - Labels: E:/KITTI/tracking/0006/label_02/0006.txt
  - Per-frame labels: E:/KITTI/_temp_extract/lbl/training/label_02/0006/*.txt

Outputs:
  - data/kitti_yolo_v1.1_clean/
    ├── images/val/
    ├── labels/val/
    ├── triplets_val.txt     # t-1, t, t+1 frame stems
    └── kitti_ghostdet_v1.1_clean.yaml

USB-safe: processes 1 frame at a time (low RAM).
Author: Ken Byrne (Dec 2025)
"""

import os
import cv2
import numpy as np
from pathlib import Path

# ── Paths ───────────────────────────────────────────────────────────────────────
IMG_SRC = Path("E:/KITTI/tracking/0006/image_02/0006")           # 270 PNGs
LBL_SRC = Path("E:/KITTI/_temp_extract/lbl/training/label_02/0006")  # From map_labels_to_seq06_v1.1_clean.py
OUT_ROOT = Path("data/kitti_yolo_v1.1_clean")
IMG_OUT = OUT_ROOT / "images/val"
LBL_OUT = OUT_ROOT / "labels/val"

OUT_ROOT.mkdir(parents=True, exist_ok=True)
IMG_OUT.mkdir(parents=True, exist_ok=True)
LBL_OUT.mkdir(parents=True, exist_ok=True)

# ── KITTI → YOLO Class Mapping ─────────────────────────────────────────────────
CLASS_MAP = {"Car": 0, "Van": 0, "Truck": 1, "Pedestrian": 2, "Cyclist": 3}
IMG_W, IMG_H = 1242, 375  # Original KITTI resolution
TARGET_W, TARGET_H = 640, 192  # Resized for YOLO

def kitti_to_yolo(line: str) -> str | None:
    """Convert KITTI label line to YOLO format (class xc yc w h)."""
    parts = line.strip().split()
    if len(parts) < 15:
        return None
    cls_name = parts[0]
    if cls_name not in CLASS_MAP:
        return None
    try:
        x1, y1, x2, y2 = map(float, parts[4:8])
        # Clamp to image bounds
        x1, x2 = max(0, x1), min(IMG_W, x2)
        y1, y2 = max(0, y1), min(IMG_H, y2)
        if x2 <= x1 or y2 <= y1:
            return None
        # Normalize
        xc = ((x1 + x2) / 2) / IMG_W
        yc = ((y1 + y2) / 2) / IMG_H
        w = (x2 - x1) / IMG_W
        h = (y2 - y1) / IMG_H
        return f"{CLASS_MAP[cls_name]} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}"
    except Exception:
        return None

# ── Main Processing ────────────────────────────────────────────────────────────
print(f" Source images: {IMG_SRC}")
print(f" Source labels: {LBL_SRC}")

# Get sorted frame stems (e.g., '000000', '000001', ..., '000269')
stems = sorted([f.stem for f in IMG_SRC.glob("*.png")])
print(f" Found {len(stems)} frames")

triplets = []
processed = 0

for i in range(1, len(stems) - 1):
    t0, t1, t2 = stems[i-1], stems[i], stems[i+1]

    # Process center frame (t1)
    img_path = IMG_SRC / f"{t1}.png"
    label_path = LBL_SRC / f"{t1}.txt"

    # Load & resize image
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"⚠️  Skip {t1}: image read failed")
        continue
    img_resized = cv2.resize(img, (TARGET_W, TARGET_H))
    out_img_path = IMG_OUT / f"0006_{t1}.jpg"
    cv2.imwrite(str(out_img_path), img_resized)

    # Process labels
    yolo_lines = []
    if label_path.exists():
        with open(label_path) as f:
            for line in f:
                yolo_line = kitti_to_yolo(line)
                if yolo_line:
                    yolo_lines.append(yolo_line)

    out_lbl_path = LBL_OUT / f"0006_{t1}.txt"
    with open(out_lbl_path, 'w') as f:
        f.write('\n'.join(yolo_lines))

    triplets.append(f"0006_{t0} 0006_{t1} 0006_{t2}")
    processed += 1

    if processed % 50 == 0:
        print(f"  ✔ Processed {processed}/{len(stems)-2} triplets")

# ── Save Outputs ───────────────────────────────────────────────────────────────
with open(OUT_ROOT / "triplets_val.txt", 'w') as f:
    f.write('\n'.join(triplets))

with open(OUT_ROOT / "kitti_ghostdet_v1.1_clean.yaml", 'w') as f:
    f.write(f"""path: ./data/kitti_yolo_v1.1_clean
train: images/val
val: images/val
nc: 4
names: ['car', 'truck', 'pedestrian', 'cyclist']
""")

print(f"\n Done.")
print(f"   → Images: {IMG_OUT}")
print(f"   → Labels: {LBL_OUT}")
print(f"   → Triplets: {len(triplets)} (for temporal evaluation)")
print(f"   → Config: {OUT_ROOT / 'kitti_ghostdet_v1.1_clean.yaml'}")