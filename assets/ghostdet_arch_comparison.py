import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
plt.title('GhostDet: YOLOv8 with GhostNet Backbone — Architecture Comparison', fontsize=14, pad=20)

# ========================
# YOLOv8n (Baseline)
# ========================
ax.text(2, 9.2, 'YOLOv8n (Baseline)', ha='center', fontweight='bold', fontsize=11)
# Backbone
ax.add_patch(FancyBboxPatch((0.5, 7.5), 3, 1.2, boxstyle="round,pad=0.2", facecolor='#f8cecc', edgecolor='k'))
ax.text(2, 8.1, 'CSPDarknet\n(3.2M params)', ha='center', va='center', fontsize=9)
# Neck
ax.add_patch(FancyBboxPatch((0.5, 6.0), 3, 1.0, boxstyle="round,pad=0.2", facecolor='#e1d5e7', edgecolor='k'))
ax.text(2, 6.5, 'PAN-FPN', ha='center', va='center', fontsize=9)
# Head
ax.add_patch(Rectangle((0.5, 4.5), 3, 0.8, facecolor='#d5e8d4', edgecolor='k'))
ax.text(2, 4.9, 'Decoupled Head', ha='center', va='center', fontsize=9)

# ========================
# GhostDet (New Model)
# ========================
ax.text(7, 9.2, 'GhostDet (New Model)', ha='center', fontweight='bold', fontsize=11, color='blue')
# Backbone → Ghost-CSP
ax.add_patch(FancyBboxPatch((5.5, 7.5), 3, 1.2, boxstyle="round,pad=0.2", facecolor='#dae8fc', edgecolor='k'))
ax.text(7, 8.1, 'Ghost-CSP\n(2.1M params)', ha='center', va='center', fontsize=9, fontweight='bold')
# Annotate Ghost Module
ax.add_patch(Rectangle((6.0, 7.7), 0.8, 0.4, facecolor='white', edgecolor='k'))
ax.text(6.4, 7.9, 'GC', ha='center', va='center', fontsize=8)
ax.text(6.4, 7.6, 'Ghost\nConv', ha='center', va='top', fontsize=7)
# Neck → Ghost-PAN
ax.add_patch(FancyBboxPatch((5.5, 6.0), 3, 1.0, boxstyle="round,pad=0.2", facecolor='#d5e8d4', edgecolor='k'))
ax.text(7, 6.5, 'Ghost-PAN', ha='center', va='center', fontsize=9, fontweight='bold')
# Head (shared)
ax.add_patch(Rectangle((5.5, 4.5), 3, 0.8, facecolor='#d5e8d4', edgecolor='k'))
ax.text(7, 4.9, 'Decoupled Head', ha='center', va='center', fontsize=9)

# ========================
# ShuffleNetV2-YOLO (Lighter)
# ========================
ax.text(12, 9.2, 'ShuffleNetV2-YOLO', ha='center', fontweight='bold', fontsize=11)
ax.add_patch(FancyBboxPatch((10.5, 7.5), 3, 1.2, boxstyle="round,pad=0.2", facecolor='#fff2cc', edgecolor='k'))
ax.text(12, 8.1, 'ShuffleNetV2\n(1.9M params)', ha='center', va='center', fontsize=9)
ax.add_patch(FancyBboxPatch((10.5, 6.0), 3, 1.0, boxstyle="round,pad=0.2", facecolor='#e1d5e7', edgecolor='k'))
ax.text(12, 6.5, 'PAN-FPN', ha='center', va='center', fontsize=9)
ax.add_patch(Rectangle((10.5, 4.5), 3, 0.8, facecolor='#d5e8d4', edgecolor='k'))
ax.text(12, 4.9, 'Decoupled Head', ha='center', va='center', fontsize=9)

# Arrows
for x in [2, 7, 12]:
    for y_start, y_end in [(8.7, 8.3), (7.5, 7.1), (6.0, 5.6)]:
        ax.add_line(Line2D([x, x], [y_start, y_end], color='k', linewidth=1))
        # Arrowhead
        ax.add_line(Line2D([x-0.1, x], [y_end, y_end+0.1], color='k'))
        ax.add_line(Line2D([x+0.1, x], [y_end, y_end+0.1], color='k'))

# Ghost Module Detail (Inset)
ax.text(7, 3.0, 'Ghost Module (Core Innovation)', ha='center', fontweight='bold', fontsize=10)
ghost_x, ghost_y = 5.5, 1.5
ax.add_patch(Rectangle((ghost_x, ghost_y+0.8), 3, 0.4, facecolor='white', edgecolor='k'))
ax.text(ghost_x+1.5, ghost_y+1.0, '1×1 Conv (Intrinsic)', ha='center', va='center', fontsize=8)
ax.add_patch(Rectangle((ghost_x, ghost_y+0.3), 3, 0.4, facecolor='white', edgecolor='k'))
ax.text(ghost_x+1.5, ghost_y+0.5, 'Depthwise Conv (Ghost)', ha='center', va='center', fontsize=8)
ax.add_patch(Rectangle((ghost_x, ghost_y), 3, 0.2, facecolor='#d5e8d4', edgecolor='k'))
ax.text(ghost_x+1.5, ghost_y+0.1, 'Concat → Output', ha='center', va='center', fontsize=8)
ax.annotate('', xy=(ghost_x+3.1, ghost_y+0.5), xytext=(ghost_x+3.5, ghost_y+0.5),
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
ax.text(ghost_x+4.0, ghost_y+0.5, '50% fewer params', color='blue', va='center', fontsize=9)

# Legend
legend_y = 0.5
legend_items = [
    ('YOLOv8 Backbone', '#f8cecc'),
    ('Ghost-CSP (new Model','#dae8fc'),
    ('Ghost-PAN', '#d5e8d4'),
    ('ShuffleNetV2', '#fff2cc')
]
for i, (text, color) in enumerate(legend_items):
    y = legend_y - i * 0.3
    ax.add_patch(Rectangle((10.5, y), 0.3, 0.2, facecolor=color, edgecolor='k'))
    ax.text(11.0, y+0.1, text, va='center', fontsize=8)

import os

# Save  
png_path = 'ghostdet_arch_comparison.png'
pdf_path = 'ghostdet_arch_comparison.pdf'

plt.savefig(png_path, dpi=300, bbox_inches='tight')
plt.savefig(pdf_path, bbox_inches='tight')

print(f" Diagram saved:")
print(f"   PNG: {os.path.abspath(png_path)}")
print(f"   PDF: {os.path.abspath(pdf_path)}")

#  interactive run
import sys
if not sys.flags.interactive:
    plt.close(fig)  # Free memory
    # Exit cleanly
    exit(0)
else:
    plt.show()