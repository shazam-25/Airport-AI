from airport_ai.config import config

class CameraConfig:
    def __init__(self, data):
        self.camera_id = data["camera_id"]
        self.camera_name = data.get(
            "camera_name",
            self.camera_id
        )
        self.source = config.resolve_path(data["source"])