from ultralytics import YOLO
import torch

# Load pretrained YOLOv8n
model = YOLO("yolov8n.pt")

# Train (5 epochs)
model.train(
    data="data/kitti_yolo/kitti_ghostdet.yaml",
    epochs=5,
    imgsz=640,
    batch=8,          # reduced for laptop
    name="ghostdet_local",
    device="cpu"      # "0" if GPU available
)

print(" Training complete. Weights saved to runs/train/ghostdet_local/weights/best.pt")