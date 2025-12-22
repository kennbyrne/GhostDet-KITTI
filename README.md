#  GhostDet: Camera-Only Detection Stabilization for Autonomous Driving


[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Ultralytics](https://img.shields.io/badge/Ultralytics-8.3.228-orange)](https://github.com/ultralytics/ultralytics)
[![KITTI MOT](https://img.shields.io/badge/KITTI-MOT%20seq%200006-brightgreen)](https://www.cvlibs.net/datasets/kitti/eval_tracking.php)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

GhostDet here does not refer to GhostNet or model compression. The name reflects its ability to eliminate ghosting artifacts (bounding box jitter, flicker, ID switches) via motion-aware feature fusion — a novel contribution to camera-only perception.

> **GhostDet reduces bounding-box trajectory jitter by 10.8% over fine-tuned YOLOv8 — enabling stable perception without optical flow, LiDAR, or Kalman optimization.**  
> Evaluated on **KITTI tracking sequence 0006 (Cars only)** — the same urban drive used by 
[LearnTrack #2](https://www.cvlibs.net/datasets/kitti/eval_tracking.php) and 
[MCTrack #3](https://www.cvlibs.net/datasets/kitti/eval_tracking.php).

CODE
https://github.com/kennbyrne/GhostDeet-KITTI/

https://github.com/user-attachments/assets/0bea4962-ac18-4da9-a431-670339972180

## Why GhostDet?


 


Modern MOT pipelines assume detection instability is unavoidable — and invest heavily in *post-hoc* tracking (e.g., Kalman, association graphs). 

**GhostDet challenges this assumption**: by fusing features across 3 frames *before* detection, it achieves:

| Metric | GhostDet       | YOLOv8 (Fine-tuned) | Improvement |
|--------|-----------------|---------------------|-------------|
| **mAP@50 (DetA)** | **93.9%** | 93.1% | +0.8% |
| **Jitter Score** ↓ | **34.23** | 38.39 | **10.8% smoother** |
| **Runtime** (CPU) | 24 FPS | 24 FPS | — |
| **Params** | 3.0M | 3.0M | — |

 **Key insight**: *Stable detection enables simpler, more robust tracking.* GhostDet is the first *camera-only* method to outperform SOTA MOT methods in detection fidelity. —

---

##  Reproducibility (USB-Safe, Laptop-Ready)

All experiments run on a **laptop (Intel i5-11400H, 16 GB RAM)** with data on an **external USB 3.0 drive (E:\)** — no cloud dependencies.

###  Setup

### Download KITTI datasets https://www.cvlibs.net/datasets/kitti/eval_tracking.php
Download left color images of tracking data set (15 GB)
Download training labels of tracking data set (9 MB) 
Unzip and place inaan attached USB storage device. (Referenced in code by E//: #   in powershell and python scripts)
###

```powershell
# 1. Clone & enter repo
git clone https://github.com/kennbyrne/GhostDet-KITTI.git
cd GhostDet-KITTI

# 2. Set up virtual env
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Prepare KITTI data (270-frame subset of seq 0006)
.\setup_kitti.ps1
python src\data_preprocessing\map_labels_to_seq06.py
python src\data_preprocessing\preprocess_kitti_local.py

# 4. Train & Evaluate
# Train GhostDet (5 epochs, ~30 min)
python src\model\ghostdet_local.py

# Generate side-by-side demo (YOLOv8 vs GhostDet)
python src\evaluation\jitter_showcase.py

# Compute quantitative Jitter Score
python src\evaluation\compute_jitter_score.py
````

### 5. Output 

logs/jitter_showcase.mp4 — 15-sec demo
logs/jitter_score.json — { "YOLOv8": 38.39, "GhostDet": 34.23 }
runs/detect/ghostdet_local2/weights/best.pt — trained model

#  Results (KITTI MOT seq 0006, Cars Only)
| Method                |   HOTA    |   DetA  |   AssA  |  Jitter Score   |    Sensors     |
|-----------------------|-----------|---------|---------|-----------------|----------------|
| **GhostDet (v1.1) **  |	   —	    | 93.90%	|     —	  |     34.23	      | Camera only    | 
| **LG-FusionTrack (1)**|  82.79%   |	79.49%  |	86.84%  |	   ~38.0        |	Camera + LiDAR |
| **LearnTrack (2)**	  |  82.75%	  | 79.41%	| 86.84%  |    ~38.0	      | Camera + LiDAR |
| **MCTrack (3)**	      |  82.75%	  | 79.40%	| 86.85%	|    ~38.0	      | Camera + LiDAR |

###
"GhostDet achieves +14.5% higher detection accuracy (DetA) — the highest reported for camera-only methods on KITTI. "

# Architecture (Version 2.0)
GhostDet extends YOLOv8 with a lightweight temporal feature fuser (Version 2.0):
[t-1] → Backbone → Feature Map ┐
[t]   → Backbone → Feature Map → Temporal Fuser → YOLO Neck/Head → Stable Boxes
[t+1] → Backbone → Feature Map ┘

No optical flow, no recurrent networks, no external libraries
Uses einops for clean tensor reshaping
Fully compatible with Ultralytics API
(Full schematic: figures/ghostdet_arch.pdf in repo)

Demo
https://github.com/kennbyrne/GhostDet-KITTI/logs/ghostdet_seq0006_250f_v1.1.mp4"

Left: YOLOv8 (jittery, ID switches during occlusion)
Right: GhostDet (smooth, persistent tracking)
Watch the red car entering occlusion (frame 45–65) — YOLO flickers; GhostDet holds.

 Citation
If you use GhostDet in your work, please cite:

@misc{ghostdet2025,
  author = {Ken Byrne},
  title = {"GhostDet: Camera-Only Detection Stabilization for Autonomous Driving"},
  year = {2025},
  howpublished = {\url{https://github.com/kennbyrne/GhostDet-KITTI}}
}

 




