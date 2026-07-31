import cv2
from pathlib import Path

class VideoSource:
    """
    Wrapper around OpenCV VideoCapture.
    Supports:
        - RTSP
        - USB camera
        - Video file
    """
    def __init__(self, source):
        self.path = str(source)
        print("Opening Video:", self.path)
        self.cap = cv2.VideoCapture(self.path)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source: {source}")
    
    def read(self):
        ret, frame = self.cap.read()
        # Cause of not reaching Video EOF
        # if not ret:
        #     # Restart video file
        #     self.cap.release()
        #     self.cap = cv2.VideoCapture(self.path)
        #     ret, frame = self.cap.read()
        return ret, frame
        

    def release(self):
        self.cap.release()