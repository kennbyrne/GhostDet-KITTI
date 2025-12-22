import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

# Ghost Module
ax.add_patch(FancyBboxPatch((1, 5), 3, 2, boxstyle="round,pad=0.3", facecolor='#dae8fc', edgecolor='#6c8ebf'))
ax.text(2.5, 6.5, 'Ghost Module', ha='center', va='center', fontweight='bold', fontsize=10)
ax.add_patch(Rectangle((1.5, 5.5), 2, 0.4, facecolor='white', edgecolor='k'))
ax.text(2.5, 5.7, '1×1 Conv (Intrinsic)', ha='center', va='center', fontsize=9)
ax.add_patch(Rectangle((1.5, 5.0), 2, 0.4, facecolor='white', edgecolor='k'))
ax.text(2.5, 5.2, 'Depthwise Conv (Ghost)', ha='center', va='center', fontsize=9)
ax.add_patch(Rectangle((1.5, 4.5), 2, 0.4, facecolor='#d5e8d4', edgecolor='k'))
ax.text(2.5, 4.7, 'Concat', ha='center', va='center', fontsize=9)

# Attention Blocks
ax.text(2.5, 4.0, 'Attention Mechanisms', ha='center', fontweight='bold', fontsize=10)
ax.add_patch(Rectangle((1.5, 3.5), 1, 0.4, facecolor='#fff2cc', edgecolor='k'))
ax.text(2.0, 3.7, 'SE', ha='center', va='center', fontsize=9)
ax.add_patch(Rectangle((2.6, 3.5), 1, 0.4, facecolor='#fff2cc', edgecolor='k'))
ax.text(3.1, 3.7, 'CBAM', ha='center', va='center', fontsize=9)
ax.add_patch(Rectangle((2.05, 3.0), 1, 0.4, facecolor='#d5e8d4', edgecolor='k'))
ax.text(2.55, 3.2, 'ECA', ha='center', va='center', fontsize=9)

# Backbone Comparison
ax.text(6, 6.8, 'Lightweight Backbones', ha='center', fontweight='bold', fontsize=10)
backbones = [
    ('GhostNet\n3.9M', '#dae8fc'),
    ('ShuffleNetV2\n2.3M', '#e1d5e7'),
    ('VoVNet\n5.5M', '#f8cecc')
]
for i, (label, color) in enumerate(backbones):
    y = 6.2 - i * 0.7
    ax.add_patch(Rectangle((5, y), 2, 0.5, facecolor=color, edgecolor='k'))
    ax.text(6, y + 0.25, label, ha='center', va='center', fontsize=9)

# Compression Pipeline
steps = [
    ('GhostNet (FP32)', '#dae8fc'),
    ('Pruning (30%)', '#d5e8d4'),
    ('Distillation', '#e1d5e7'),
    ('QAT (INT8)', '#fff2cc'),
    ('TensorRT / ONNX', '#f8cecc')
]
for i, (step, color) in enumerate(steps):
    y = 6.2 - i * 0.7
    rect = Rectangle((8.5, y), 2, 0.5, facecolor=color, edgecolor='k')
    ax.add_patch(rect)
    ax.text(9.5, y + 0.25, step, ha='center', va='center', fontsize=9)
    if i < len(steps) - 1:
        # Draw downward arrow
        ax.add_line(Line2D([9.5, 9.5], [y, y - 0.15], color='k', linewidth=1))
        # Arrowhead
        ax.add_line(Line2D([9.5, 9.4], [y - 0.15, y - 0.1], color='k', linewidth=1))
        ax.add_line(Line2D([9.5, 9.6], [y - 0.15, y - 0.1], color='k', linewidth=1))

# Legend
legend_y = 2.0
ax.text(9.5, legend_y + 0.3, 'Legend', ha='center', fontweight='bold', fontsize=10)
legend_items = [
    ('Ghost Module', '#dae8fc'),
    ('Pruning/Distil', '#d5e8d4'),
    ('Attention', '#fff2cc'),
    ('Backend', '#f8cecc')
]
for i, (text, color) in enumerate(legend_items):
    y = legend_y - i * 0.4
    ax.add_patch(Rectangle((8.8, y), 0.3, 0.3, facecolor=color, edgecolor='k'))
    ax.text(9.2, y + 0.15, text, va='center', fontsize=9)

plt