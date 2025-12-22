# GhostDet-KITTI Versioning Policy

To ensure reproducibility and clarity during rapid iteration, this project uses **lightweight filename-based versioning** for scripts and models.

## Script Versioning

All Python scripts follow the pattern:  
`{name}_v{MAJOR}.{MINOR}.py`

| Component | Meaning | Example |
|----------|---------|---------|
| `{name}` | Descriptive base name | `demo_video_local` |
| `v{MAJOR}` | Breaking change in logic/output | `v2` = True GhostDet (YOLO + Infuser) vs `v1` = identical models |
| `{MINOR}` | Parameter tuning, robustness, bugfix | `_v2.1` = tuned `alpha`, added occlusion decay |

### Examples
- `demo_video_local_v1.0.py`: Baseline — YOLOv8n (untuned) vs fine-tuned YOLO (same weights).
- `demo_video_local_v2.0.py`: True GhostDet — YOLO + `GhostInfuser`.
- `ghost_infuser_v1.0.py`: First implementation of temporal smoother.

## When to Increment

| Change | Increment |
|-------|-----------|
| New architecture (e.g., triplet backbone) | `MAJOR++` |
| Parameter tuning (e.g., `alpha=0.6` → `0.7`) | `MINOR++` |
| Path robustness, logging, docstring | `MINOR++` |
| Bugfix (no output change) | `MINOR++` |

##  Folder Structure
src/
    ├── evaluation/ # Active scripts (e.g., demo_video_local_v2.0.py)
    ├── model/ # Core models (e.g., ghost_infuser_v1.0.py)
    ├── data_preprocessing/ # Pipeline scripts (e.g., preprocess_kitti_local_v1.0.py)
    └── utils/checks_balances/ # Diagnostics, bulk tools

## Reproducibility

- All `v1.0` scripts are archived in-place (no separate `version/` folders).
- Evaluation outputs (videos, `jitter_score.json`) are written to `figures/`.
- Model weights are saved to `runs/detect/{name}/weights/best.pt`.
- Archived outputs (v1.0) stored in figures/version1.0/ and src/evaluation/version1.0/.

> This policy balances agility and traceability
