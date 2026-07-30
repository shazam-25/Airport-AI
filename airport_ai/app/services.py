from dataclasses import dataclass
from airport_ai.dashboard.runtime_store import runtime_store

@dataclass
class SharedServices:
    """
    Shared application services.
    Only one instance of each service is created and reused
    by every CameraPipeline.
    """
    database: object
    repository: object
    storage_writer: object
    alert_repository: object
    alert_manager: object
    visualizer: object
    inference_engine: object
    tracker_factory: object
    turnaround_factory: object
    ppe_factory: object
    fod_factory: object
    analytics_executor: object
    profiler: object | None = None


class DashboardService:

    def __init__(
        self,
        pipelines,
        repository
    ):
        self.pipelines = pipelines
        self.repository = repository
        self.runtime_store = runtime_store


    def get_frame(
        self,
        camera_id
    ):

        pipeline = self.pipelines.get(camera_id)

        if pipeline is None:
            return None

        return pipeline.latest_frame



    def get_metrics(
        self,
        camera_id
    ):

        pipeline = self.pipelines.get(camera_id)

        if pipeline is None:
            return None

        return pipeline.metrics.health()



    def get_objects(
        self,
        camera_id
    ):

        pipeline = self.pipelines.get(camera_id)

        if pipeline is None:
            return []

        return pipeline.latest_tracks



    def get_events(
        self,
        camera_id
    ):

        pipeline = self.pipelines.get(camera_id)

        if pipeline is None:
            return {}

        return pipeline.latest_events