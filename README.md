Airport-AI
|- airport_ai
|   |- alerts
|       |- __init__.py
|       |- manager.py
|       |- models.py
|       |- notifier.py
|       |- priority.py
|       |- repository.py
|   |- analytics "READY"
|       |- __init__.py
|       |- executor.py
|   |- app
|       |- __init__.py
|       |- application.py
|       |- builder.py
|       |- runner.py
|       |- services.py
|   |- config
|       |- __init__.py
|       |- camera.py
|       |- config.yaml
|       |- loader.py
|       |- schemas.py
|       |- settings.py
|   |- dashboard
|       |- __init__.py
|       |- app.py
|       |- components.py
|       |- database.py
|       |- video.py
|   |- decision "READY"
|       |- fod -> (LATER CHANGE) evaluator classes
|           |- __init__.py
|           |- evaluator.py -> FODEvaluator -> return FODEvent (s)
|           |- monitor.py -- NOT REQUIRED
|           |- selector.py -- NOT REQUIRED
|           |- structures.py -- NOT REQUIRED
|           |- visualization.py -- NOT REQUIRED
|       |- ppe
|           |- __init__.py
|           |- association.py -> class PPEAssociation (CHANGE LATER)
|           |- evaluator.py -> PPEEvaluator (CHANGE LATER) -> return PPEEvent (s)
|           |- selector.py --- NOT REQUIRED
|           |- status.py -> dataclass PPEStatus
|           |- visualization.py -- NOT REQUIRED
|       |- turnaround
|           |- __init__.py
|           |- aircraft.py -- NOT REQUIRED
|           |- evaluator.py -> class TurnaroundEvaluator -> return SafetyEvent (s) (CHANGE LATER)
|           |- structures.py -- NOT REQUIRED
|           |- visualization.py -- NOT REQUIRED
|           |- zone.py -> class SafetyZone
|   |- inference -- READY
|       |- __init__.py
|       |- detection.py -> class Detection "READY"
|       |- strcutures.py "READY"
|       |- tracked_object.py -> TrackedObject -> return tracked_object "RE"
|       |- yolo_engine.py -> class YOLOEngine -> return detections "READY"
|   |- performance
|       |- __init__.py
|       |- metrics.py
|       |- profiler.py
|       |- time.py
|   |- pipeline
|       |- __init__.py
|       |- camera_pipeline.py
|       |- manager.py
|   |- storage
|       |- __init__.py
|       |- cache.py
|       |- database.py
|       |- repository.py
|       |- schema.py
|       |- writer.py
|   |- streams
|       |- __init__.py
|       |- buffer.py
|       |- camera.py
|       |- video_source.py
|   |- tracking -- READY
|       |- __init__.py
|       |- parser.py "READY"
|       |- strcutures.py "READY"
|       |- tracker.py -> class ObjectTracker "READY"
|   |- utils
|       |- common.py
|       |- drawing.py
|       |- geometry.py
|   |- visualization
|       |- __init__.py
|       |- draw_utils.py_
|       |- overlay_cache.py
|       |- visualizer.py
|- tools
|       |- extract_frames.py
|       |- train_aiport.py