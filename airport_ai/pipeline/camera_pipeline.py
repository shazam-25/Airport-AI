import cv2
import numpy as np

from airport_ai.performance.timer import Timer
from airport_ai.performance.metrics import RuntimeMetrics
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
    ):
        self.camera_id = camera_config.camera_id
        self.camera_name = camera_config.camera_name
        self.source = camera_config.source

        self.camera = frame_buffer
        self.inference_engine = inference_engine
        self.tracker = tracker

        self.turnaround = turnaround
        self.ppe = ppe
        self.fod = fod

        self.repository = repository
        self.storage_writer = storage_writer
        self.alert_manager = alert_manager
        self.visualizer = visualizer
        self.analytics_executor = analytics_executor

        self.profiler = profiler

        self.metrics = RuntimeMetrics(camera_id=self.camera_id)

        self.frame_skip = config.get("processing")["frame_skip"]

        self.frame_count = 0
        self.frame_index = 0

        self.processed_frames = 0
        self.skipped_frames = 0
        self.dropped_frames = 0

        self._previous_gray = None

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
                self.storage_writer.submit(self.camera_id, stream, event)
                self.alert_manager.create_alert(stream, event)
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
            camera_name=self.camera_name,
            tracks=tracks,
            safety_events=safety_events,
            ppe_events=ppe_events,
            fod_events=fod_events,
            fps=fps
        )
        visualization_time = timer.stop()
        if self.profiler:
            self.profiler.record("visualization", visualization_time)

        # ===================
        # Runtime Metrics
        # ===================
        total_time = pipeline_timer.stop()
        self.metrics.update_frame(total_time)
        self.frame_count += 1
        self.processed_frames += 1

        if (self.profiler and self.frame_count % config.get("performance")["summary_interval"] == 0):
            print("\n====== PERFORMANCE REPORT ======")
            report = self.profiler.summary()
            for stage, values in report.items():
                print(
                    f"{stage:<25}"
                    f"{values['avg_ms']:.2f} ms"
                )
        
        print("\n===== RUUNTIME METRICS =====")
        print(self.metrics.health())

        self.profiler.reset()

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
            "camera_id": self.camera_id,
            "processed_frames": self.processed_frames,
            "skipped_frames": self.skipped_frames,
            "dropped_frames": self.dropped_frames,
            "queue_size": (self.camera.size() if hasattr(self.camera, "size") else 0,)
        }
