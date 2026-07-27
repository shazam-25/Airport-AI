import cv2

class PPEVisualizer:
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    WHITE = (255, 255, 255)

    def draw_worker(self, frame, person): # Draw worker bounding box
        cv2.rectangle(
            frame,
            (int(person.x1), int(person.y1)),
            (int(person.x2), int(person.y2)),
            self.BLUE,
            2
        )
        return frame

    def draw_track_id(self, frame, person):
        cv2.putText(
            frame, 
            f"ID {person.track_id}",
            (int(person.x1), int(person.y1)-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            self.WHITE,
            2
        )
        return frame
    
    def status_text(self, status):
        vest = "V✓" if status.safety_vest else "V✗"
        ear = "E✓" if status.ear_protection else "E✗"
        return f"{vest} {ear}"

    def draw_ppe_status(self, frame, status):
        text = self.status_text(status)
        cv2.putText(
            frame,
            text,
            (int(status.person.x1), int(status.person.y2)+20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            self.YELLOW,
            2
        )
        return frame

    def compliant(self, status):
        return(
            status.safety_vest
            and 
            status.ear_protection
        )

    def draw_compliance(self, frame, status):
        color = self.GREEN if self.compliant(status) else self.RED
        text = "COMPLIANT" if self.compliant(status) else "NON-COMPLIANT"
        cv2.putText(
            frame,
            text,
            (int(status.person.x1), int(status.person.y2)+45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )
        return frame

    def draw_events(self, frame, events):
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

    def draw(self, frame, statuses, events):
        for status in statuses:
            self.draw_worker(frame, status.person)
            self.draw_track_id(frame, status.person)
            self.draw_ppe_status(frame, status)
            self.draw_compliance(frame, events)
        self.draw_events(frame, events)
        return frame