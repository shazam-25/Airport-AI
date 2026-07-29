from dataclasses import dataclass

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