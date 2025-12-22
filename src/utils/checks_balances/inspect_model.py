# inspect_model.py
from ultralytics import YOLO
import torch

print("🔍 Loading model: runs/detect/ghostdet_local2/weights/best.pt")
model = YOLO("runs/detect/ghostdet_local2/weights/best.pt")
m = model.model

print(f"✅ Model type: {type(m).__name__}")
print(f"✅ Total modules: {len(list(m.modules()))}\n")

print("=== Backbone layers (first 10 named children) ===")
for i, (name, layer) in enumerate(m.named_children()):
    if i >= 10:
        break
    print(f"{i:2d}: {name:<12} | {layer.__class__.__name__}")

print("\n=== Searching for Ghost/Temporal clues ===")
ghost_kw = ['ghost', 'bottleneck', 'depthwise', 'cheap']
temporal_kw = ['temporal', 'fuse', 'stack', 'frame', 'infuser', 'sliding']

found = []
for name, module in m.named_modules():
    cls_name = module.__class__.__name__.lower()
    full_name = name.lower()
    for kw in ghost_kw + temporal_kw:
        if kw in cls_name or kw in full_name:
            found.append((name, module.__class__.__name__))
            break  # avoid dupes

if found:
    for name, cls in found[:10]:
        print(f"🎯 {name} → {cls}")
else:
    print("⚠️ No explicit ghost/temporal modules found — may be fused or in forward hook.")

# Try forward pass
try:
    print("\n⏯️ Testing forward pass (batch=1, 640x640)...")
    dummy = torch.rand(1, 3, 640, 640)
    with torch.no_grad():
        output = m(dummy)
    if isinstance(output, (list, tuple)):
        print(f"✅ Forward succeeded. Output len: {len(output)}")
        for i, o in enumerate(output[:3]):
            print(f"   → output[{i}].shape = {o.shape}")
    else:
        print(f"✅ Forward succeeded. Output shape: {output.shape}")
except Exception as e:
    print(f"❌ Forward failed: {e}")

print("\n🔍 Inspection complete.")