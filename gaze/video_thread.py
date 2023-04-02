import time

import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal

from gaze.mediapipe_utils import HeadPoseEstimation


class VideoThread(QThread):  # https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
    gaze_img_change_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        pose_estimation = HeadPoseEstimation()
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                cv_img = pose_estimation.head_pose_estimation(cv_img)
                self.gaze_img_change_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class OuterVideoThread(QThread):
    lane_img_change_signal = pyqtSignal(np.ndarray)
    start_time_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        start_time = time.time()
        headPoseEstimation = HeadPoseEstimation()
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                cv_img = headPoseEstimation.head_pose_estimation(cv_img)
                self.lane_img_change_signal.emit(cv_img)
                # self.start_time_signal.emit(start_time)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
