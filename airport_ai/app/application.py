class AirportAIApplication:
    def __init__(
        self,
        pipelines,
        services,
        runtime_store
    ):
        self.pipelines = pipelines
        self.services = services
        self.runtime_store=runtime_store

    def run(self):
        """
        Starts all camera pipelines.
        """
        print(f"Starting {len(self.pipelines)} camera(s)")
        active = dict(self.pipelines)
        while active:
            finished = []
            for camera_id, pipeline in active.items():
                frame = pipeline.process_frame()
                if frame is not None:
                    print(
                        f"{camera_id}: frame processed"
                    )
                camera = pipeline.camera
                if (
                    not camera.running and camera.buffer.empty()
                ):
                    print(f"{camera_id} completed.")
                    finished.append(camera_id)
            for camera_id in finished:
                pipeline = active.pop(camera_id)
                pipeline.camera.stop()
            if not active: break
        self.shutdown()
    
    # def display(self, camera_id, frame):
    #     # Dashboard integration later
    #     pass
    
    def stop(self): # Video stop if EOF
        for pipeline in self.pipelines.values():
            if hasattr(pipeline.camera, "stop"):
                pipeline.camera.stop()

            if hasattr(pipeline.camera, "release"):
                pipeline.camera.release()
    
    def shutdown(self):
        for pipeline in self.pipelines.values():
            pipeline.analytics_executor.shutdown()

    def get_metrics(self):
        return [
            pipeline.metrics.health()
            for pipeline in self.pipelines.values()
        ]

    def get_processing_stats(self):
        return [
            pipeline.processing_stats()
            for pipeline in self.pipelines.values()
        ]

    def get_pipeline(self, camera_id):
        return self.pipelines.get(camera_id)

    def get_runtime_store(self):
        return self.runtime_store

    def dashboard_snapshot(self):
        snapshot = {}

        for camera_id, pipeline in self.pipelines.items():
            snapshot[camera_id] = {
                "frame": pipeline.latest_frame,
                "tracks": pipeline.latest_tracks,
                "events": pipeline.latest_events,
                "metrics": pipeline.metrics.health(),
            }

        return snapshot

    def start(self):
        for pipeline in self.pipelines.values():
            pipeline.start()

    

    

    