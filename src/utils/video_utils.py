# src/utils/video_utils.py
"""
Video utilities for GhostDet v1.1_clean:
- Clean side-by-side rendering (titles in bars, bboxes + scores in frame)
- Optional low-confidence highlighting (e.g., red for <60%)
- Optional occlusion-aware labeling (e.g., 'car*' — disabled by default)
"""

import cv2
import numpy as np
from ultralytics.engine.results import Results


def safe_plot(
    results: Results,
    conf=True,
    labels=True,
    boxes=True,
    font_scale=0.5,
    line_width=2,
    img=None,
    highlight_low_conf: bool = True,
    occlusion_aware: bool = False
) -> np.ndarray:
    """
    Plot with ONLY bboxes + class + confidence (e.g., 'car 87.3').
    
    Args:
        highlight_low_conf: If True, confidence <60% in red (else white).
        occlusion_aware: If True, append '*' for occluded objects (e.g., 'car*').
                        KITTI occlusion levels: 0=fully, 1=partly, 2=mostly; >0 → occluded.
    """
    # Start with standard YOLO plot (compact, well-positioned)
    plotted = results.plot(
        conf=conf,
        labels=labels,
        boxes=boxes,
        font_size=font_scale,
        line_width=line_width,
        img=img
    )

    # If no boxes, return as-is
    if len(results.boxes) == 0:
        return plotted

    # Optionally enhance with custom styling
    for i, box in enumerate(results.boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf_val = float(box.conf[0])
        cls_id = int(box.cls[0])

        # --- Confidence text ---
        conf_text = f"{conf_val * 100:.1f}"
        color = (0, 0, 255) if (highlight_low_conf and conf_val < 0.6) else (255, 255, 255)

        # --- Class text (with optional occlusion marker) ---
        class_name = results.names[cls_id]
        if occlusion_aware and hasattr(box, 'data') and box.data.shape[1] > 5:
            # KITTI-derived labels may store occlusion in data[:,5] (0=visible, 1/2=occluded)
            occlusion = int(box.data[0, 5]) if box.data.shape[1] > 5 else 0
            if occlusion > 0:
                class_name += "*"

        # Combine: 'car 87.3' or 'car* 87.3'
        label_text = f"{class_name} {conf_text}"

        # Position: slightly inside top-left corner
        cv2.putText(
            plotted, label_text,
            (x1 + 4, y1 + 16),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
            color, 1, cv2.LINE_AA
        )

    return plotted


def add_video_borders(
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    left_title: str = "YOLOv8 (Untuned)",
    right_title: str = "GhostDet (Fine-tuned)",
    status_text: str = "",
    top_bar_h: int = 36,
    bottom_bar_h: int = 30,
    font = cv2.FONT_HERSHEY_SIMPLEX,
    font_scale: float = 0.75
) -> np.ndarray:
    """
    Add clean top/bottom bars for titles and status — no text in image area.
    """
    h, w = left_frame.shape[:2]
    total_w = w * 2
    total_h = h + top_bar_h + bottom_bar_h

    # Dark neutral background (GitHub Dark inspired)
    canvas = np.full((total_h, total_w, 3), (28, 31, 34), dtype=np.uint8)

    # Place frames
    canvas[top_bar_h:top_bar_h + h, :w] = left_frame
    canvas[top_bar_h:top_bar_h + h, w:] = right_frame

    # Top bar: titles (YOLO orange, GhostDet green)
    cv2.putText(
        canvas, left_title,
        (int(w * 0.03), top_bar_h - 10),
        font, font_scale, (255, 165, 0), 2, cv2.LINE_AA
    )
    cv2.putText(
        canvas, right_title,
        (w + int(w * 0.03), top_bar_h - 10),
        font, font_scale, (0, 220, 120), 2, cv2.LINE_AA
    )

    # Bottom bar: status (light gray)
    if status_text.strip():
        cv2.putText(
            canvas, status_text,
            (int(w * 0.03), total_h - 10),
            font, font_scale * 0.9, (220, 220, 220), 1, cv2.LINE_AA
        )

    return canvas