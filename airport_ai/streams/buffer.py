from queue import Queue
from threading import Lock

class FrameBuffer:
    """
    Thread-safe bounded frame queue.
    Stores frames only.
    Drops the oldest frame when full.
    """
    def __init__(self, maxsize=10):
        self.queue = Queue(maxsize=maxsize)
        self.lock = Lock()

    def put(self, frame):
        with self.lock:
            if self.queue.full():
                self.queue.get_nowait()
            self.queue.put_nowait(frame)

    def read(self):
        if self.queue.empty():
            return None
        return self.queue.get()

    # def get(self):
    #     return self.queue.get()

    def empty(self):
        return self.queue.empty()

    def size(self):
        return self.queue.qsize()
        # return 0

    def drop_oldest(self):
        if self.queue.empty():
            return
        self.queue.get_nowait()