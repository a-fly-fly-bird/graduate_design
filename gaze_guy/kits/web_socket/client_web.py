import cv2
import requests
import numpy as np

url = 'http://localhost:5000/video_feed'
# 打开摄像头并准备读取视频流
cap = cv2.VideoCapture(url)
if not cap.isOpened():
    print('无法打开视频流')
    exit(0)

# 读取视频流并展示图像
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Video Stream', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()
