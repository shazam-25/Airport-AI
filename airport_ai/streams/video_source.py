import cv2

class VideoSource:
    """
    Wrapper around OpenCV VideoCapture.
    Supports:
        - RTSP
        - USB camera
        - Video file
    """
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source: {source}")
    
    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()