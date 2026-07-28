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
        alert_manager,
        visualizer,
        profiler=None,
    ):
        self.camera_id = camera_config.camera_id
        self.camera_name = camera_config.camera_name
        self.source = camera_config.source

        self.buffer = frame_buffer
        self.inference_engine = inference_engine
        self.tracker = tracker

        self.turnaround = turnaround
        self.ppe = ppe
        self.fod = fod

        self.repository = repository
        self.alert_manager = alert_manager
        self.visualizer = visualizer

        self.profiler = profiler
        self.frame_count = 0
        self.metrics = RuntimeMetrics(camera_id=self.camera_id)

    def process_frame(self):
        # Measure Total Pipeline Latency
        pipeline_timer = Timer()
        pipeline_timer.start()

        # Read next frame
        timer = Timer()
        
        # ================
        # Capture
        # ================
        timer.start()
        frame = self.buffer.read()
        if hasattr(self.buffer, "size"):
            self.metrics.update_queue(self.buffer.size())
        elapsed = timer.stop()

        if self.profiler:
            self.profiler.record("capture", elapsed)
        
        if frame is None:
            return None
        
        # ================
        # YOLO
        # ================
        timer.start()
        detections = self.inference_engine.detect(frame)
        elapsed = timer.stop()

        if self.profiler:
            self.profiler.record("yolo", elapsed)

        # =================
        # Tracking
        # =================
        timer.start()
        tracks = self.tracker.update(detections)
        elapsed = timer.stop()
        
        if self.profiler:
            self.profiler.record("tracking", elapsed)
        
        # ===================
        # Decision Streams
        # ===================
        # -- 1. Turnaround --
        timer.start()
        safety_events = self.turnaround.evaluate(tracks)
        elapsed = timer.stop()
        if self.profiler:
            self.profiler.record("turnaround", elapsed)
        # -- 2. PPE
        timer.start()
        ppe_events = self.ppe.evaluate(tracks)
        elapsed = timer.stop()
        if self.profiler:
            self.profiler.record("ppe", elapsed)
        # -- 3. FOD
        timer.start()
        fod_events = self.fod.evaluate(tracks)
        elapsed = timer.stop()
        if self.profiler:
            self.profiler.record("fod", elapsed)

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
                self.repository.save(self.camera_id, stream, event)
                self.alert_manager.create_alert(stream, event)
        
        elapsed = timer.stop()
        if self.profiler.record("storage_alerts", elapsed)
        
        # ===================
        # Visualization
        # ===================
        timer.start()
        output = self.visualizer.draw(
            frame,
            tracks,
            safety_events,
            ppe_events,
            fod_events,
        )
        elapsed = timer.stop()
        if self.profiler:
            self.profiler.record("visualization, elapsed")

        self.frame_count += 1

        if (self.profiler and self.frame_count % config["performance"]["summary_interval"] == 0):
            print("\n====== PERFORMANCE REPORT ======")
            report = self.profiler.summary()
            for stage, values in report.items():
                print(
                    f"{stage:<20}"
                    f"{values['avg_ms']:.2f} ms"
                )

        self.profiler.reset()
        total_time = pipeline_timer.stop()
        self.metrics.update_frame(total_time)
        print("\n===== RUUNTIME METRICS =====")
        print(self.metrics.health())

        return output
