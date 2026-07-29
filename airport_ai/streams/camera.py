import cv2
import threading
import queue

from airport_ai.streams.buffer import FrameBuffer
from airport_ai.streams.video_source import VideoSource

class AsyncCamera:
    def __init__(self,
        source, 
        width=1280, 
        height=720, 
        queue_size=10, 
        frame_skip=1
    ):
        self.source = VideoSource(source)
        self.buffer = FrameBuffer(queue_size)
        self.width = width
        self.height = height
        self.frame_skip = frame_skip
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()
        return self
    
    def stop(self):
        self.running = False
        self.thread.join()
        self.source.release()

    def update(self):
        frame_count = 0
        while self.running:
            ret, frame = self.source.read()
            if not ret:
                print(
                "Video ended:",
                self.source.path
                )
                self.running = False
                break
            frame_count += 1
            if frame_count % self.frame_skip != 0:
                continue
            frame = cv2.resize(frame, (self.width, self.height),)
            self.buffer.put(frame)

    def read(self):
        return self.buffer.read()
