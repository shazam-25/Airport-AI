from airport_ai.app.application import AirportAIApplication
from airport_ai.app.services import SharedServices
from airport_ai.pipeline.camera_pipeline import CameraPipeline
from airport_ai.config.camera import CameraConfig
from airport_ai.streams.buffer import FrameBuffer

class ApplicationBuilder:
    def __init__(self, config):
        self.config = config
    
    def build(self):
        """
        Returns a fully initialized AirportAIApp.
        """
        services = self.create_services()
        pipelines = self.create_camera_pipelines(services)
        return AirportAIApplication(pipelines=pipelines)

    def create_services(self):
        # ==============
        # Database
        # ==============
        from airport_ai.storage.database import Database
        database_config = self.config.get("database")
        database = Database(database_config["path"])

        # =============
        # Repositories
        # =============
        from airport_ai.storage.repository import EventRepository
        repository = EventRepository(database)

        # ================
        # Alert Repository
        # ================
        from airport_ai.alerts.repository import AlertRepository
        alert_repository = AlertRepository(database)

        # ================
        # Alert Manager
        # ================
        from airport_ai.alerts.manager import AlertManager
        from airport_ai.alerts.notifier import ConsoleNotifier

        notifier = ConsoleNotifier()

        alert_manager = AlertManager(alert_repository, notifier)

        # ======================
        # YOLO Inference Engine
        # ======================
        from airport_ai.inference.yolo_engine import YOLOEngine

        model_config = self.config.get("model")

        inference_engine = YOLOEngine(
            model_path=model_config["path"],
            confidence=model_config["confidence"],
            device=model_config["device"],
        )

        # ====================
        # Tracker
        # ====================
        from airport_ai.tracking.tracker import ObjectTracker

        tracker_factory = lambda: ObjectTracker(
            model_path=self.config.get("tracking")["model_path"]
        )

        # =====================
        # Visualizer
        # =====================
        from airport_ai.visualization.visualizer import Visualizer
        visualizer = Visualizer()

        # =================
        # Profiler
        # =================
        profiler = None
        performance = self.config.get("performance")
        if performance["profiling"]["enabled"]:
            from airport_ai.performance.profiler import PipelineProfiler
            profiler = PipelineProfiler()

        # ===============
        # Factories
        # ===============
        from airport_ai.decision.turnaround.evaluator import TurnaroundEvaluator
        from airport_ai.decision.ppe.evaluator import PPEEvaluator
        from airport_ai.decision.fod.evaluator import FODEvaluator

        return SharedServices(
            database=database,
            repository=repository,
            alert_repository=alert_repository,
            alert_manager=alert_manager,
            visualizer=visualizer,
            inference_engine=inference_engine,
            tracker_factory=tracker_factory,
            turnaround_factory=lambda camera_id: TurnaroundEvaluator(
                camera_id=camera_id
            ),
            ppe_factory=lambda camera_id: PPEEvaluator(
                camera_id=camera_id
            ),
            fod_factory=lambda camera_id: FODEvaluator(
                camera_id=camera_id
            ),
            profiler=profiler,
        )
    
    def create_camera_pipelines(self, services):
        pipelines = []
        camera_configs = [
            CameraConfig(camera) for camera in self.config.get("cameras")
        ]
        for camera_config in camera_configs:
            buffer = FrameBuffer(camera_config.source)
            pipeline = CameraPipeline(
                camera_config=camera_config,
                frame_buffer=buffer,
                inference_engine=services.inference_engine,
                tracker=services.tracker_factory(),
                turnaround=services.turnaround_factory(
                    camera_config.camera_id
                ),
                ppe=services.ppe_factory(
                    camera_config.camera_id
                ),
                fod=services.fod_factory(
                    camera_config.camera_id
                ),
                repository=services.repository,
                alert_manager=services.alert_manager,
                visualizer=services.visualizer,
                profiler=services.profiler
            )
            pipelines.append(pipeline)
        return pipelines
