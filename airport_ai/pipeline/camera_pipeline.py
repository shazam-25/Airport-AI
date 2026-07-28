class CameraPipeline:
    def __init__(
        self,
        camera_config,
        tracker,
        turnaround,
        ppe,
        fod,
        repository
    ):
        self.camera_id = camera_config.camera_id
        self.camera_name = camera_config.camera_name
        self.source = camera_config.source
        self.tracker = tracker
        self.turnaround = turnaround
        self.ppe = ppe
        self.fod = fod
        self.repository = repository