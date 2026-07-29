from airport_ai.app.application import AirportAIApplication
from airport_ai.app.services import SharedServices
from airport_ai.pipeline.camera_pipeline import CameraPipeline
from airport_ai.config.camera import CameraConfig
from airport_ai.streams.camera import AsyncCamera
from airport_ai.analytics.executor import AnalyticsExecutor

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
        database_path = self.config.resolve_path(database_config["path"])
        database = Database(database_config["path"])

        # =================
        # Event Repository
        # =================
        from airport_ai.storage.repository import EventRepository
        from airport_ai.storage.writer import StorageWriter
        repository = EventRepository(database)
        storage_writer = StorageWriter(repository)

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

        tracker_factory = lambda: ObjectTracker()

        # =================
        # Profiler
        # =================
        profiler = None
        performance = self.config.get("performance")
        if performance["profiling"]["enabled"]:
            from airport_ai.performance.profiler import PipelineProfiler
            profiler = PipelineProfiler()

        # =====================
        # Visualizer
        # =====================
        from airport_ai.visualization.visualizer import Visualizer
        visualization_config = self.config.get("visualization")
        if visualization_config is None:
            visualization_config = {}
        visualizer = Visualizer(
            config=visualization_config,
            profiler=profiler,
        )

        # ================
        # Analytics
        # ================
        analytics_executor = AnalyticsExecutor(max_workers=3)

        # ===============
        # Factories
        # ===============
        from airport_ai.decision.turnaround.evaluator import TurnaroundEvaluator
        from airport_ai.decision.ppe.evaluator import PPEEvaluator
        from airport_ai.decision.fod.evaluator import FODEvaluator

        
        return SharedServices(
            database=database,
            repository=repository,
            storage_writer=storage_writer,
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
            analytics_executor=analytics_executor,
            profiler=profiler,
        )
    
    def create_camera_pipelines(self, services):
        pipelines = []
        camera_configs = [
            CameraConfig(camera) for camera in self.config.get("cameras")
        ]
        for camera_config in camera_configs:
            camera = AsyncCamera(source=camera_config.source)
            camera.start()
            pipeline = CameraPipeline(
                camera_config=camera_config,
                frame_buffer=camera,
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
                storage_writer=services.storage_writer,
                alert_manager=services.alert_manager,
                visualizer=services.visualizer,
                analytics_executor=services.analytics_executor,
                profiler=services.profiler
            )
            pipelines.append(pipeline)
        return pipelines
