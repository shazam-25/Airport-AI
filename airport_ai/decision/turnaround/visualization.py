import cv2

class TurnaroundVisualizer:
    def draw_zone(self, frame, zone):
        cv2.rectangle(
            frame,
            (int(zone.x1), int(zone.y1)),
            (int(zone.x2), int(zone.y2)),
            (0, 255, 255),
            2
        )
        return frame