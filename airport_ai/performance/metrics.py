from time import time
from collections import deque

class RuntimeMetrics:
    def __init__(self, camera_id, window_size=100):
        self.camera_id = camera_id
        self.frame_times = deque(maxlen=window_size)
        self.latencies = deque(maxlen=window_size)
        self.frames_processed = 0
        self.start_time = time()
        self.queue_size = 0
        self.last_frame_time = None

    def update_frame(self, processing_time):
        now = time()
        self.frames_processed += 1
        self.frame_times.append(now)
        self.latencies.append(processing_time)
        self.last_frame_time = now
    
    def update_queue(self, queue_size):
        self.queue_size = queue_size

    def fps(self):
        if len(self.frame_times) < 2:
            return 0

        print(self.frame_times)

        elapsed = (self.frame_times[-1] - self.frame_times[0])

        print("Elapsed:", elapsed)
        print("Frames:", len(self.frame_times))

        if elapsed == 0:
            return 0

        return (
            len(self.frame_times) / elapsed
        )
    
    def average_latency_ms(self):
        if not self.latencies:
            return 0

        return (
            sum(self.latencies) / len(self.latencies)
        ) * 1000

    def health(self):
        return {
            "camera_id": self.camera_id,
            "fps": round(self.fps(), 2),
            "latency_ms": round(self.average_latency_ms(), 2),
            "queue_size": self.queue_size,
            "frames_processed": self.frames_processed,
            "status": self.status()
        }
    

    def status(self):
        fps = self.fps()
        if fps == 0:
            return "STOPPED"
        if fps < 5:
            return "WARNING"
        return "HEALTHY"