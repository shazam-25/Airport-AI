from airport_ai.inference.structures import Detection

class DetectionParser:
    def parse(self, result):
        detections = []
        names = result.names
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            width = x2 - x1
            height = y2 - y1
            center_x = x1 + width / 2
            center_y = y1 + height / 2
            detections.append(
                Detection(
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
        return detections