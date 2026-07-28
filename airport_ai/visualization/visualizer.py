import cv2

class Visualizer:
    def __init__(self):
        pass

    def draw(
        self,
        frame,
        tracks,
        safety_events,
        ppe_events,
        fod_events,
    ):
        output = frame.copy()

        # =======================
        # Draw tracked objects
        # =======================
        if tracks:
            for obj in tracks:
                x1, y1, x2, y2 = obj.bbox
                cv2.rectangle(
                    output,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )
                cv2.putText(
                    output,
                    f"ID:{obj.track_id}",
                    (int(x1), int(y1)-5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )
        
        # ======================
        # Safety Alerts
        # ======================
        y = 30
        for event in safety_events:
            cv2.putText(
                output,
                f"SAFETY: {event.event_type}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )
            y += 30

        # ===================
        # PPE Alerts
        # ===================
        for event in ppe_events:
            cv2.putText(
                output,
                f"PPE: {event.event_type}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 165, 255),
                2
            )
            y += 30
        
        # ========================
        # FOD Alerts
        # ========================
        for event in fod_events:
            cv2.putText(
                output,
                f"FOD: {event.event_type}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )
            y += 30
        
        return output