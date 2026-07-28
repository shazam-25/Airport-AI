import cv2

class FODVisualizer:
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)

    def draw(self, frame, statuses, events):
        for status in statuses:
            obj = status.object
            color = self.RED if status.is_fod else self.GREEN
            cv2.rectangle(
                frame,
                (int(obj.x1), int(obj.y1)),
                (int(obj.x2), int(obj.y2)),
                color,
                2
            )
            label = (
                f"{obj.class_name} "
                f"{status.stationary_seconds:.1f}s"
            )
            cv2.putText(
                frame,
                label,
                (int(obj.x1), int(obj.y1)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )
        y = 30
        for event in events:
            cv2.putText(
                frame,
                event.message,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                self.RED,
                2
            )

            y += 25

        return frame