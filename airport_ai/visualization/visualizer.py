import cv2

from airport_ai.visualization.overlay_cache import OverlayCache
from airport_ai.visualization.draw_utils import (
    draw_bbox, draw_label, draw_event, draw_camera_info
)

class Visualizer:
    def __init__(self, config=None, profiler=None):
        self.config = config or {}
        self.profiler = profiler
        self.cache = OverlayCache()
        self.previous_tracks = {}
        self.label_cache = {}
        self.render_counter = 0

    # ========================
    # Main Render Function
    # ========================
    def render(
        self,
        frame,
        camera_name,
        tracks,
        safety_events,
        ppe_events,
        fod_events,
        fps=None
    ):
        self.render_counter += 1
        render_every = (
            self.config.get("render_every", 1)
        )
        if self.render_counter % render_every != 0:
            if self.profiler:
                self.profiler.visualization_skipped()
            return frame
        output = self.get_background(frame)
        self.draw_tracks(output, tracks)
        self.draw_events(output, safety_events, ppe_events, fod_events)
        draw_camera_info(output, camera_name, fps)
        if self.profiler:
            self.profiler.visualization_rendered()
        return output

    # ===========================
    # Cached Background
    # ===========================
    def get_background(self, frame):
        if (
            not self.cache.has_overlay() or self.cache.frame_shape != frame.shape
        ):
            overlay = frame.copy()
            self.draw_static(overlay)
            self.cache.store(overlay, frame.shape)
            if self.profiler:
                self.profiler.visualization_cache_miss()
            else:
                if self.profiler:
                    self.profiler.visualization_cache_hit()
        return self.cache.get().copy()

    # ===========================
    # Static Drawing
    # ===========================
    def draw_static(self, frame):
        cv2.putText(
            frame,
            "Aiport AI Monitoring",
            (20, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
    
    # ===========================
    # Tracks
    # ===========================
    def draw_tracks(self, frame, tracks):
        if not tracks: return
        for obj in tracks:
            previous = self.previous_tracks.get(obj.track_id)
            if (previous is not None and previous == obj.bbox):
                pass
            self.previous_tracks[obj.track_id] = obj.bbox
            draw_bbox(frame, obj.bbox)
            label = self.get_label(obj)
            draw_label(frame, obj.bbox, label,)
    
    # ===========================
    # Events
    # ===========================
    def draw_events(
        self,
        frame,
        safety_events,
        ppe_events,
        fod_events
    ):
        y = 40
        for event in safety_events:
            draw_event(
                frame,
                f"SAFETY : {event.event_type}",
                y,
                (0, 0, 255),
            )
            y += 30
        for event in ppe_events:
            draw_event(
                frame,
                f"PPE : {event.event_type}",
                y,
                (0, 165, 255),
            )
            y += 30
        for event in fod_events:
            draw_event(
                frame,
                f"FOD : {event.event_type}",
                y,
                (255, 0, 0),
            )
            y += 30
    
    # ===========================
    # Cached Labels
    # ===========================
    def get_label(self, obj):
        if obj.track_id not in self.label_cache:
            self.label_cache[obj.track_id] = (
                f"ID:{obj.track_id}"
            )
        return self.label_cache[obj.track_id]

    # ===========================
    # Cache Reset
    # ===========================
    def clear_cache(self):
        self.cache.invalidate()
        self.previous_tracks.clear()
        self.label_cache.clear()


    # def draw(
    #     self,
    #     frame,
    #     tracks,
    #     safety_events,
    #     ppe_events,
    #     fod_events,
    # ):
    #     output = frame.copy()

    #     # =======================
    #     # Draw tracked objects
    #     # =======================
    #     if tracks:
    #         for obj in tracks:
    #             x1, y1, x2, y2 = obj.bbox
    #             cv2.rectangle(
    #                 output,
    #                 (int(x1), int(y1)),
    #                 (int(x2), int(y2)),
    #                 (0, 255, 0),
    #                 2
    #             )
    #             cv2.putText(
    #                 output,
    #                 f"ID:{obj.track_id}",
    #                 (int(x1), int(y1)-5),
    #                 cv2.FONT_HERSHEY_SIMPLEX,
    #                 0.5,
    #                 (0, 255, 0),
    #                 2
    #             )
        
    #     # ======================
    #     # Safety Alerts
    #     # ======================
    #     y = 30
    #     for event in safety_events:
    #         cv2.putText(
    #             output,
    #             f"SAFETY: {event.event_type}",
    #             (20, y),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             0.7,
    #             (0, 0, 255),
    #             2
    #         )
    #         y += 30

    #     # ===================
    #     # PPE Alerts
    #     # ===================
    #     for event in ppe_events:
    #         cv2.putText(
    #             output,
    #             f"PPE: {event.event_type}",
    #             (20, y),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             0.7,
    #             (0, 165, 255),
    #             2
    #         )
    #         y += 30
        
    #     # ========================
    #     # FOD Alerts
    #     # ========================
    #     for event in fod_events:
    #         cv2.putText(
    #             output,
    #             f"FOD: {event.event_type}",
    #             (20, y),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             0.7,
    #             (255, 0, 0),
    #             2
    #         )
    #         y += 30
        
    #     return output
