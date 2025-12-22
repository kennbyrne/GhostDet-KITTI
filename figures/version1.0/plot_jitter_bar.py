# jitter score bar chart
import json
import matplotlib.pyplot as plt

# Load results
with open("logs/jitter_score.json", "r") as f:
    data = json.load(f)

# Extract values
methods = ["YOLOv8\n(fine-tuned)", "GhostDet\n(temporal)"]
jitter = [data["YOLOv8_fine_tuned"], data["GhostDet_temporal"]]
colors = ["#e74c3c", "#2ecc71"]  # red (YOLO), green (GhostDet)

# Create plot
plt.figure(figsize=(4.5, 4))
bars = plt.bar(methods, jitter, color=colors, width=0.6, edgecolor='black', linewidth=1)

# Annotate values
for i, (bar, val) in enumerate(zip(bars, jitter)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
             f"{val:.1f}", ha='center', va='bottom', fontsize=12, fontweight='bold')

# Styling
plt.ylabel("Jitter Score (px/frame) ↓", fontsize=12)
plt.title("Trajectory Smoothness on KITTI Sequence 0006", fontsize=13, pad=20)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.ylim(0, max(jitter) * 1.15)

# Add arrow
yolo_val = jitter[0]
ghost_val = jitter[1]
plt.annotate(f"{data['improvement_percent']:.1f}%\n smoother",
             xy=(1, ghost_val), xytext=(0, yolo_val - 3),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
             fontsize=11, ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.9))

# Save high-res
plt.tight_layout()
plt.savefig("figures/jitter_score_bar.pdf", bbox_inches='tight', dpi=300)
plt.savefig("figures/jitter_score_bar.png", bbox_inches='tight', dpi=300)
print("✅ Saved: figures/jitter_score_bar.pdf & .png")

# plt.show()