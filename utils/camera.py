import cv2

def get_camera(source=0):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise Exception("❌ Cannot access webcam")

    return cap