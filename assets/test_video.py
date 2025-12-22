# test_video.py
import cv2
cap = cv2.VideoCapture("logs/ghostdet_vs_yolov8_local.mp4")
ret, frame = cap.read()
print("Video read success:", ret)
if ret:
    print("Frame shape:", frame.shape)
cap.release()