# debug_plots.py
from pathlib import Path

# List all runs
print(" Scanning for validation runs...")
runs = list(Path("runs/detect").glob("val*"))
ghost_runs = list(Path("runs/detect").glob("ghostdet*"))

print("\nValidation runs:")
for r in runs:
    txt = r / "results.txt"
    csv = r / "results.csv"
    print(f"  {r.name}: results.txt={txt.exists()}, results.csv={csv.exists()}")

print("\nGhostDet runs:")
for r in ghost_runs:
    txt = r / "results.txt"
    csv = r / "results.csv"
    val_txt = r / "val/results.txt"
    print(f"  {r.name}: results.txt={txt.exists()}, results.csv={csv.exists()}, val/results.txt={val_txt.exists()}")