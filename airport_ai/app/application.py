class AirportAIApplication:
    def __init__(self, pipelines):
        self.pipelines = pipelines

    def run(self):
        """
        Starts all camera pipelines.
        """
        print(f"Starting {len(self.pipelines)} camera(s)")
        while True:
            for pipeline in self.pipelines:
                frame =  pipeline.process_frame()
                if frame is not None:
                    self.display(pipeline.camera_id, frame)
    
    def display(self, camera_id, frame):
        # Dashboard integration later
        pass
    
    def stop(self):
        """
        Stops all camera pipelines.
        """
        for pipeline in self.pipelines:
            pipeline.buffer.release()

    def get_metrics(self):
        results = []
        for pipeline in self.pipelines:
            results.append(pipeline.metrics.health())
        return results

    def get_processing_stats(self):
        return [
            pipeline.processing_stats() for pipeline in self.pipelines
        ]

    def shutdown(self):
        for pipeline in self.pipelines:
            pipeline.analytics_executor.shutdown()