from posix import eventfd
import cv2
import numpy as np

from airport_ai.performance.timer import Timer
from airport_ai.performance.metrics import RuntimeMetrics
from airport_ai.events.event_memory import EventMemory
from airport_ai.config import config

class CameraPipeline:
    def __init__(
        self,
        camera_config,
        frame_buffer,
        inference_engine,
        tracker,
        turnaround,
        ppe,
        fod,
        repository,
        storage_writer,
        alert_manager,
        visualizer,
        analytics_executor,
        profiler=None,
        runtime_store=None
    ):  
        self.camera_config = camera_config
        # self.camera_id = camera_config.camera_id
        # self.camera_name = camera_config.camera_name
        # self.source = camera_config.source

        self.camera = frame_buffer
        self.inference_engine = inference_engine
        self.tracker = tracker

        self.turnaround = turnaround
        self.ppe = ppe
        self.fod = fod

        self.repository = repository
        self.storage_writer = storage_writer
        self.alert_manager = alert_manager
        self.event_memory = EventMemory(config.get("events")["cooldown_seconds"])
        self.visualizer = visualizer
        self.analytics_executor = analytics_executor

        self.profiler = profiler

        self.runtime_store = runtime_store

        self.metrics = RuntimeMetrics(camera_id=self.camera_config.camera_id)

        self.frame_skip = config.get("processing")["frame_skip"]

        # self.frame_count = 0
        self.frame_index = 0

        self.processed_frames = 0
        self.skipped_frames = 0
        self.dropped_frames = 0

        self._previous_gray = None
        self.latest_frame = None

        # Latest detections
        self.latest_tracks = []

        # Latest events
        self.latest_events = {
            "TURNAROUND": [],
            "PPE": [],
            "FOD": []
        }
        

    # =====================
    # Main Pipeline
    # =====================
    def process_frame(self):
        self.frame_index += 1

        # --- Frame Skipping --
        if self.frame_skip > 0:
            if self.frame_index % (self.frame_skip + 1) != 1:
                self.skipped_frames += 1
                self.tracker.predict_only()
                return None

        # Measure Total Pipeline Latency
        pipeline_timer = Timer()
        pipeline_timer.start()

        # Read next frame
        timer = Timer()

        # --- Queue Backpressue (Drop oldest frame) ---
        max_queue = config.get("processing")["max_queue_size"]
        while (
            hasattr(self.camera, "size") and self.camera.size() > max_queue
        ):
            self.camera.drop_oldest()
            self.dropped_frames += 1

        # ================
        # Capture
        # ================
        timer.start()
        frame = self.camera.read()
        capture_time = timer.stop()
        if self.profiler:
            self.profiler.record("capture", capture_time)
        if frame is None:
            return None
        if hasattr(self.camera, "size"):
            self.metrics.update_queue(self.camera.size())
        # --- Duplicate Frame Check ---
        if self.is_duplicate_frame(frame):
            self.skipped_frames += 1
            self.tracker.predict_only()
            return None
        
        # ================
        # YOLO
        # ================
        timer.start()
        detections = self.inference_engine.detect(frame)
        inference_time = timer.stop()
        if self.profiler:
            self.profiler.record("yolo", inference_time)

        # =================
        # Tracking
        # =================
        timer.start()
        tracks = self.tracker.update(detections)
        tracking_time = timer.stop()
        if self.profiler:
            self.profiler.record("tracking", tracking_time)
        
        # ===================
        # Parallel Analytics
        # ===================
        timer.start()
        (
            safety_events,
            ppe_events,
            fod_events,
        ) = self.analytics_executor.evaluate(
            tracks,
            self.turnaround,
            self.ppe,
            self.fod
        )
        analytics_time = timer.stop()
        if self.profiler:
            self.profiler.record("analytics_parallel", analytics_time)

        # ====================
        # Store + Alert
        # ====================
        events = [
            ("TURNAROUND", safety_events),
            ("PPE", ppe_events),
            ("FOD", fod_events)
        ]
        timer.start()
        for stream, stream_events in events:
            for event in stream_events:
                key = (
                    f"{stream}_"
                    f"{event.event_type}_"
                    f"{event.track_id}"
                )
                # prevent duplicate alerts
                if not self.event_memory.allow(key):
                    continue
                self.storage_writer.submit(self.camera_config.camera_id, stream, event)
                self.alert_manager.create_alert(stream, event)
                if self.runtime_store:  # DASHBOARD
                    self.runtime_store.save_event(event)
        storage_time = timer.stop()
        if self.profiler:
            self.profiler.record("storage_alerts", storage_time)
        
        # ===================
        # Visualization
        # ===================
        timer.start()
        fps = self.metrics.fps()
        output = self.visualizer.render(
            frame=frame,
            camera_name=self.camera_config.camera_name,
            tracks=tracks,
            safety_events=safety_events,
            ppe_events=ppe_events,
            fod_events=fod_events,
            fps=fps
        )
        # =====================
        # Dashboard State Update
        # =====================
        # self.latest_frame = output
        # self.latest_tracks = tracks
        # self.latest_events = {
        #     "TURNAROUND": safety_events,
        #     "PPE": ppe_events,
        #     "FOD": fod_events
        # }
        # if self.runtime_store:
        #     self.runtime_store.save_frame(
        #         self.camera_config.camera_id,
        #         output
        #         # output.copy()
        #     )
        #     print("RuntimeStore updated:", self.camera_config.camera_id)
        # if self.runtime_store:    Duplicate save events 
        #     for event_group in (
        #         safety_events,
        #         ppe_events,
        #         fod_events
        #     ):
        #         for event in event_group:
        #             self.runtime_store.save_event(event)

        visualization_time = timer.stop()
        if self.profiler:
            self.profiler.record("visualization", visualization_time)

        # ===================
        # Runtime Metrics
        # ===================
        total_time = pipeline_timer.stop()
        print("Updating metrics")
        self.metrics.update_frame(total_time)
        if hasattr(self.camera, "size"):
            self.metrics.update_queue(self.camera.size())
        # if self.runtime_store:
        #     self.runtime_store.update_metrics(
        #         self.camera_config.camera_id,
        #         self.metrics.health()
        #     )
        # print(self.metrics.health())
        # if self.runtime_store:
        #     self.runtime_store.update_metrics(
        #         self.camera_config.camera_id,
        #         self.metrics.health()
            # )
        # self.frame_count += 1
        self.processed_frames += 1

        if (self.profiler and self.processed_frames % config.get("performance")["summary_interval"] == 0):
            print("\n====== PERFORMANCE REPORT ======")
            report = self.profiler.summary()
            for name, values in report.items():
                avg_ms = (
                    values.get("avg_ms")
                    or values.get("average_ms")
                    or values.get("avg")
                    or 0
                )
                print(
                    f"{name:<25}"
                    f"{avg_ms:.2f} ms"
                )
        
        print("\n===== RUUNTIME METRICS =====")
        print(self.metrics.health())

        # self.profiler.reset()

        print(f"Capture: {capture_time*1000:.2f} ms")
        print(f"YOLO: {inference_time*1000:.2f} ms")
        print(f"Tracking: {tracking_time*1000:.2f} ms")
        print(f"Analytics: {analytics_time*1000:.2f} ms")
        print(f"Storage: {storage_time*1000:.2f} ms")
        print(f"Visualization: {visualization_time*1000:.2f} ms")

        # self.latest_frame = output  # Dashboard

        return output

    # =========================
    # Duplicate frame Detection
    # =========================
    def is_duplicate_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self._previous_gray is None:
            self._previous_gray = gray
            return False
        
        difference = np.mean(
            cv2.absdiff(gray, self._previous_gray)
        )
        self._previous_gray = gray
        threshold = config.get("processing")["duplicate_threshold"]
        return difference < threshold

    # ====================
    # Statistics
    # ====================
    def processing_stats(self):
        return {
            "camera_id": self.camera_config.camera_id,
            "processed_frames": self.processed_frames,
            "skipped_frames": self.skipped_frames,
            "dropped_frames": self.dropped_frames,
            "queue_size": (self.camera.size() if hasattr(self.camera, "size") else 0,)
        }
