"""
Application Launcher
"""

from airport_ai.runtime.camera_worker import CameraWorker
from airport_ai.runtime.stream_manager import StreamManager


stream_manager = StreamManager()


worker = CameraWorker(
    pipeline=pipeline,
    camera_id="GATE_A01",
    output_buffer=stream_manager.frames
)


worker.start()