from airport_ai.tracking.structures import TrackedObject

class TrackingParser:
    def parse(self, result):
        tracked_objects = []
        names = result.names
        if result.boxes.id is None:
            return tracked_objects
        for box in result.boxes:
            track_id = int(box.id[0])
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            width = x2 - x1
            height = y2 - y1
            center_x = x1 + width / 2
            center_y =  y1 + height / 2
            tracked_objects.append(
                TrackedObject(
                    track_id=track_id,
                    class_id=class_id,
                    class_name=names[class_id],
                    confidence=confidence,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    center_x=center_x,
                    center_y=center_y,
                    width=width,
                    height=height
                )
            )
        return tracked_objects