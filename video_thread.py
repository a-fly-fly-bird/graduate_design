import cv2
import numpy as np
import mediapipe as mp

from PyQt6.QtCore import QThread, pyqtSignal

from mediapipe_utils import HeadPoseEstimation


class VideoThread(QThread):  # https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
    gaze_img_change_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        pose_estimation = HeadPoseEstimation(mp_drawing, mp_drawing_styles)
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

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        pose_estimation = HeadPoseEstimation(mp_drawing, mp_drawing_styles)
        cap = cv2.VideoCapture(1)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                cv_img = pose_estimation.head_pose_estimation(cv_img)
                self.lane_img_change_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()