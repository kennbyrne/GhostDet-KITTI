#!/usr/bin/env python3
"""
find_ghostinfuser.py
Search for temporal infuser / smoothing logic in GhostDet evaluation scripts.
Scans src/evaluation/ for keywords: smooth, fuse, infuse, history, deque, occlusion, holdover.
Designed for GhostDet-KITTI project.
"""

import os
import re
from pathlib import Path

# Config
SEARCH_DIRS = [
    Path("src/evaluation"),
    Path("src/model"),
    Path("assets")
]
KEYWORDS = [
    r"\bsmooth", r"\bfuse", r"\binfuse", r"\bhistory",
    r"\bdeque", r"\bocclusion", r"\bhold", r"\btemporal",
    r"\bema", r"\btrack", r"\bassociate", r"\biou"
]

def main():
    print(" Scanning for GhostInfuser implementation clues...\n")
    matches = []

    for root in SEARCH_DIRS:
        if not root.exists():
            print(f"⚠  Skipping (not found): {root}")
            continue

        print(f" Scanning: {root}")
        for py_file in root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                print(f"    Skip {py_file}: {e}")
                continue

            for i, line in enumerate(lines):
                line_clean = line.strip()
                if not line_clean or line_clean.startswith('#'):
                    continue

                for kw in KEYWORDS:
                    if re.search(kw, line, re.IGNORECASE):
                        # Show context: up to 2 lines before/after
                        start = max(0, i - 1)
                        end = min(len(lines), i + 2)
                        context = [f"{'→' if j==i else ' '} {j+1:3d}: {lines[j].rstrip()}" 
                                  for j in range(start, end)]
                        matches.append((py_file, i+1, line_clean, context))
                        break  # one match per line

    # Report
    if matches:
        print(f"\n Found {len(matches)} candidate locations:\n")
        for file, lineno, snippet, ctx in matches:
            rel_path = file.relative_to(Path.cwd())
            print(f" {rel_path}:{lineno}")
            for c in ctx:
                print(f"    {c}")
            print()
    else:
        print("\n  No GhostInfuser logic found. Consider adding src/model/ghost_infuser.py")

    print(" Scan complete.")

if __name__ == "__main__":
    main()