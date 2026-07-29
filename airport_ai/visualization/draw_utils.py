import cv2

# ======================
# Bounding Box
# ======================
def draw_bbox(
    frame,
    bbox,
    color=(0, 255, 0),
    thickness=2,
):
    """
    Draw a bounding box.
    """
    x1, y1, x2, y2 = map(int, bbox)
    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        thickness,
    )

# ======================
# Labels
# ======================
def draw_label(
    frame,
    bbox,
    text,
    color=(0, 255, 0),
):
    """
    Draw a label above the bounding box.
    """
    x1, y1, _, _ = map(int, bbox)
    cv2.putText(
        frame,
        text,
        (x1, max(y1 - 8, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        color,
        2,
        cv2.LINE_AA,
    )

# ======================
# Safety Zone
# ======================
def draw_zone(
    frame,
    bbox,
    color=(255, 255, 0),
    thickness=2,
):
    """
    Draw the aircraft safety zone.
    """
    x1, y1, x2, y2 = map(int, bbox)
    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        thickness,
    )

# ======================
# Generic Event Text
# ======================
def draw_event(
    frame,
    text,
    y,
    color,
):
    """
    Draw an event message on the left side of the screen.
    """
    cv2.putText(
        frame,
        text,
        (20, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        color,
        2,
        cv2.LINE_AA,
    )

# ======================
# Camera Information
# ======================
def draw_camera_info(
    frame,
    camera_name,
    fps=None,
):
    """
    Draw camera metadata.
    """
    cv2.putText(
        frame,
        f"Camera : {camera_name}",
        (20, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    if fps is not None:
        cv2.putText(
            frame,
            f"FPS : {fps:.1f}",
            (20, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

# ======================
# Status Badge
# ======================
def draw_status(
    frame,
    text,
    position,
    color=(255, 255, 255),
):
    """
    Draw a small status label.
    """
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        color,
        2,
        cv2.LINE_AA,
    )

# ======================
# Filled Banner
# ======================
def draw_banner(
    frame,
    text,
    color=(0, 0, 255),
):
    """
    Draw a filled warning banner.
    """
    h, w = frame.shape[:2]
    cv2.rectangle(
        frame,
        (0, 0),
        (w, 35),
        color,
        -1,
    )
    cv2.putText(
        frame,
        text,
        (10, 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )