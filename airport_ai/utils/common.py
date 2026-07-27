import cv2

def show(frame):
    cv2.imshow("Airport AI", frame)
    if cv2.waitKey(1) == 27:
        return False
    return True