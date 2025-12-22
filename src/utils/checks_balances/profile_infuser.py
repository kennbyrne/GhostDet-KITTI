import time
from ultralytics import YOLO
from src.model.ghost_infuser import GhostInfuser

model = YOLO("runs/detect/ghostdet_local2/weights/best.pt")
infuser = GhostInfuser()
img = cv2.imread("sample.jpg")
res = model(img)[0]

N = 100
times = []
for _ in range(N):
    t0 = time.perf_counter()
    _ = infuser.smooth(res)
    times.append((time.perf_counter() - t0) * 1000)

print(f"GhostInfuser: {np.mean(times):.2f} ± {np.std(times):.2f} ms/frame (N={N})")