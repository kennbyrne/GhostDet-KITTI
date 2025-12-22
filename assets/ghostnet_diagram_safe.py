import matplotlib
matplotlib.use('Agg')  # Force for windows
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

try:
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Minimal content to verify it works
    ax.text(6, 7, ' GhostDet Architecture Diagram', ha='center', fontsize=14, fontweight='bold')
    ax.text(6, 6, 'Ghost Module: Intrinsic + Ghost Features', ha='center', fontsize=11)
    ax.add_patch(Rectangle((4, 4), 4, 1, facecolor='#dae8fc', edgecolor='k'))
    ax.text(6, 4.5, '1×1 Conv → DW Conv → Concat', ha='center', va='center')

    ax.text(6, 2, 'Saved to:\n' + __file__.replace('ghostnet_diagram_safe.py', 'ghostnet_diagram_safe.png'),
            ha='center', fontsize=9, style='italic')

    # SAVE 
    png_path = 'ghostnet_diagram_safe.png'
    pdf_path = 'ghostnet_diagram_safe.pdf'
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    
    print(f" SUCCESS!")
    print(f"   PNG saved: {png_path}")
    print(f"   PDF saved: {pdf_path}")

    try:
        plt.show()
    except Exception as e:
        print(f"  Display not available: {e}")

except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()