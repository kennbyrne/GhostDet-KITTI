# inspect_kitti.py — Diagnose KITTI folder structure
import os
from pathlib import Path

def inspect_kitti(root_path="E:/KITTI"):
    root = Path(root_path)
    if not root.exists():
        print(f" Root '{root}' does not exist.")
        return

    print(f" Scanning KITTI at: {root}\n")
    found_seqs = {}

    # Common KITTI layouts to search
    patterns = [
        root / "tracking" / "*" / "image_02",           # tracking/0006/image_02
        root / "training" / "image_02" / "*",           # training/image_02/0006
        root / "data_tracking_image_2" / "training" / "image_02" / "*",
        root / "*" / "image_02",                        # loose folders
    ]

    for pattern in patterns:
        for img_dir in root.glob(str(pattern.relative_to(root))):
            if not img_dir.is_dir():
                continue
            seq_name = img_dir.parent.name if "tracking" in str(img_dir) else img_dir.name
            pngs = list(img_dir.glob("*.png"))
            jpgs = list(img_dir.glob("*.jpg"))
            total_imgs = len(pngs) + len(jpgs)

            # Skip tiny folders
            if total_imgs < 10:
                continue

            # Get label count (if labels exist)
            label_dir = img_dir.parent / "label_02" if "image_02" in str(img_dir) else img_dir.parent.parent / "label_02"
            labels = list(label_dir.glob("*.txt")) if label_dir.exists() else []
            label_count = len(labels)

            # Record
            found_seqs[seq_name] = {
                "path": str(img_dir),
                "frames": total_imgs,
                "labels": label_count,
                "type": "tracking" if "tracking" in str(img_dir) else "detection"
            }

    # Report
    if not found_seqs:
        print("  No KITTI image sequences found.")
        return

    print(f"{'Seq':<6} {'Frames':<8} {'Labels':<8} {'Type':<10} Path")
    print("-" * 70)
    for seq, info in sorted(found_seqs.items(), key=lambda x: x[0]):
        print(f"{seq:<6} {info['frames']:<8} {info['labels']:<8} {info['type']:<10} {info['path']}")

    # Highlight seq 0006
    if "0006" in found_seqs:
        info = found_seqs["0006"]
        print(f"\n seq 0006 found ({info['type']}): {info['frames']} frames")
        if info["frames"] >= 1100:
            print("    This is the full bus-turn sequence (use this one!)")
        else:
            print("    Short clip — may not contain full turn event")
    else:
        print("\n seq 0006 not found. Expected paths:")
        print("   - E:/KITTI/tracking/0006/image_02/")
        print("   - E:/KITTI/data_tracking_image_2/training/image_02/0006/")

    # Suggest fix for your script
    if "0006" in found_seqs:
        img_path = found_seqs["0006"]["path"]
        print(f"\n🔧 Use this path in demo_video_full.py:\n   img_dir = Path(r\"{img_path}\")")

if __name__ == "__main__":
    inspect_kitti()