from airport_ai.performance.profiler import PipelineProfiler
from airport_ai.config import config
class MultiCameraManager:
    def __init__(self, pipelines):
        self.pipelines = pipelines

    def run(self):
        while True:
            for pipeline in self.pipelines:
                pipeline.process_frame()

if __name__ == "__main__":
    performance_config = config.get("performance")
    profiler = None
    if performance_config["profiling"]["enabled"]:
        profiler = PipelineProfiler()
    pipelines = []
    cameras = config.get("cameras")
    for camera in cameras:
        pipelines.append(
            CameraPipeline(
                camera_id=config["camera_id"],
                source=config["source"],
                tracker=tracker,
                turnaround=turnaround,
                ppe=ppe,
                fod=fod,
                repository=respository,
                profiler=profiler,
            )
        )