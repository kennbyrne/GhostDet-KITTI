"""
map_labels_to_seq06_v1.1_clean.py
Maps KITTI tracking labels (0006.txt) to per-frame YOLO label files.
- Supports canonical KITTI MOT paths: tracking/0006/{image_02,label_02}
- Outputs to _temp_extract for preprocessing compatibility.

Inputs:
  - E:/KITTI/tracking/0006/label_02/0006.txt
  - E:/KITTI/tracking/0006/image_02/ (1147 PNGs)

Outputs:
  - E:/KITTI/_temp_extract/lbl/training/label_02/0006/{000000.txt, ..., 001146.txt}

Author: Kenneth Byrne (Dec 2025)
Version: v1.1_clean
"""

import os
from pathlib import Path

def find_kitti_drive():
    """Auto-detect KITTI drive (E: fallback to D: or C:)"""
    for drive in ['E', 'D', 'C']:
        base = Path(f"{drive}:/KITTI")
        if (base / "tracking/0006/image_02").exists():
            return drive, base
    raise FileNotFoundError("KITTI/tracking/0006/image_02 not found on E:/, D:/, or C:/")

DRIVE_LETTER, BASE = find_kitti_drive()
print(f" KITTI found on {DRIVE_LETTER}:")

# Canonical paths (KITTI MOT structure)
IMG_DIR = Path("E:/KITTI/tracking/0006/image_02/0006")
LABEL_FILE = Path("E:/KITTI/tracking/0006/label_02/0006.txt")
LABEL_DST = Path("E:/KITTI/_temp_extract/lbl/training/label_02/0006")

# Validate
assert IMG_DIR.exists(), f" Image dir not found: {IMG_DIR}"
assert LABEL_FILE.exists(), f" Label file not found: {LABEL_FILE}"

# Get image stems (e.g., '000000', '000001', ..., '001146')
image_stems = sorted([f.stem for f in IMG_DIR.glob("*.png")])
print(f" Found {len(image_stems)} images in {IMG_DIR}")

# Parse label file: {frame_id: [line1, line2, ...]}
frame_labels = {}
with open(LABEL_FILE, 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 16:
            continue
        try:
            frame_id = int(parts[0])
            # Skip frame_id, track_id → keep: type, truncated, occluded, alpha, bbox, etc.
            label_line = " ".join(parts[2:])
            frame_labels.setdefault(frame_id, []).append(label_line)
        except ValueError:
            continue

print(f" Parsed labels for {len(frame_labels)} frames from {LABEL_FILE.name}")

# Ensure output dir exists
LABEL_DST.mkdir(parents=True, exist_ok=True)

# Write per-frame label files
written = 0
for stem in image_stems:
    frame_id = int(stem)
    out_path = LABEL_DST / f"{stem}.txt"
    if frame_id in frame_labels:
        with open(out_path, 'w') as f:
            f.write("\n".join(frame_labels[frame_id]))
        written += 1
    else:
        # Create empty file (YOLO requires one per image)
        out_path.touch()

print(f"  Wrote {written} non-empty + {len(image_stems) - written} empty label files to {LABEL_DST}")
print(f" Next: Run src/data_preprocessing/preprocess_kitti_local_v1.1_clean.py")