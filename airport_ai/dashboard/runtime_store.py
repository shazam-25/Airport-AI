from threading import Lock


class RuntimeStore:

    def __init__(self):
        self.lock = Lock()

        self.frames = {}
        self.metrics = {}
        self.events = []

    def update_frame(self, camera_id, frame):
        with self.lock:
            self.frames[camera_id] = frame

    def get_frame(self, camera_id):
        with self.lock:
            return self.frames.get(camera_id)

    def update_metrics(self, camera_id, metrics):
        with self.lock:
            self.metrics[camera_id] = metrics

    def get_metrics(self):
        with self.lock:
            return dict(self.metrics)

    def add_event(self, event):
        with self.lock:
            self.events.append(event)
            self.events = self.events[-500:]

    def get_events(self):
        with self.lock:
            return list(self.events)


# -------- Singleton --------

runtime_store = RuntimeStore()