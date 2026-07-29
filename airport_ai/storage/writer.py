import queue
import threading
import time

class StorageWriter:
    def __init__(self, repository, batch_size=50):
        self.repository = repository
        self.batch_size = batch_size
        self.queue = queue.Queue()
        self.running = True

        self.thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.thread.start()

    def submit(self, camera_id, stream, event):
        self.queue.put((camera_id, stream, event))

    def _worker(self):
        while self.running:
            batch = []
            try:
                while len(batch) < self.batch_size:
                    batch.append(self.queue.get(timeout=0.5))
            except queue.Empty:
                pass
            if batch:
                # self.repository.save_batch(batch)
                for camera_id, stream, event in batch:
                    try:
                        self.repository.save(
                            camera_id, stream, event
                        )
                    except Exception as e:
                        print("Storage error: e")
            time.sleep(0.01)
    
    def shutdown(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()