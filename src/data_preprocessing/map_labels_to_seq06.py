"""
map_labels_to_seq06.py — Map KITTI tracking labels to sequence 0006 frames

Purpose:
    Converts KITTI tracking labels (0006.txt) into per-frame .txt files
    for YOLO format training. This enables detection-only training on full sequences.

Inputs:
    - E:/KITTI/data_tracking_label_2/training/label_02/0006.txt (tracking labels)
    - E:/KITTI/_temp_extract/img/training/image_02/0006/ (270 frames)

Outputs:
    - E:/KITTI/_temp_extract/lbl/training/label_02/0006/ (269 label files)

How to Run:
    python src/data_preprocessing/map_labels_to_seq06.py

Author: Kenneth Byrne (Nov 2025)
"""

import os
from pathlib import Path

DRIVE_LETTER = "E"
BASE = Path(f"{DRIVE_LETTER}:/KITTI")

# Path
IMG_DIR = BASE / "_temp_extract/img/training/image_02/0006"
TRACKING_LABEL_FILE = BASE / "data_tracking_label_2/training/label_02/0006.txt"
LABEL_DST = BASE / "_temp_extract/lbl/training/label_02/0006"

# Validate
assert IMG_DIR.exists(), f" IMG_DIR not found: {IMG_DIR}"
assert TRACKING_LABEL_FILE.exists(), f" Tracking labels not found: {TRACKING_LABEL_FILE}"

# image count
image_stems = [f.stem for f in IMG_DIR.glob("*.png")]
print(f" Found {len(image_stems)} images in seq 0006")

# Parse tracking label file
frame_labels = {}
with open(TRACKING_LABEL_FILE) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 16: continue
        frame_id = int(parts[0])
        # KITTI tracking label: [frame, track_id, type, ... bbox]
        label_line = " ".join(parts[2:])  # skip frame_id, track_id
        if frame_id not in frame_labels:
            frame_labels[frame_id] = []
        frame_labels[frame_id].append(label_line)

print(f"Parsed {len(frame_labels)} frames from 0006.txt")

# Create output dir
LABEL_DST.mkdir(parents=True, exist_ok=True)

# Write per-frame labels
written = 0
for stem in image_stems:
    frame_id = int(stem)
    if frame_id in frame_labels:
        out_path = LABEL_DST / f"{stem}.txt"
        with open(out_path, 'w') as f:
            f.write("\n".join(frame_labels[frame_id]))
        written += 1

print(f" Wrote {written} label files to {LABEL_DST}")
if written < len(image_stems):
    print(f"{len(image_stems) - written} frames missing labels (likely occluded/DontCare)")