# !/usr/bin/python

from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
import sys
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

import numpy as np
import sys
import mediapipe as mp

from mediapipe_utils import HeadPoseEstimation


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        # 参考：https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
        cvImg = np.random.randint(low=1, high=255, size=(300, 300, 3), dtype=np.uint8)
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
        # pixmap = QPixmap('sid.jpg')
        pixmap = QPixmap(qImg)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Sid')
        self.show()


# https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

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
                self.change_pixmap_signal.emit(cv_img)
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

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.screenwidth = None
        self.screenheight = None
        self.screenRect = None
        self.lane_img = None
        self.gaze_img = None
        self.init_ui()

    def init_ui(self):
        # fit screen
        self.screenRect = QApplication.primaryScreen().geometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()
        self.disply_width = self.screenwidth // 3
        self.display_height = self.screenheight // 3
        lane_text = QLabel("Lane Detection")
        gaze_text = QLabel("Gaze Estimation")

        self.lane_img = QLabel(self)
        filename = "/Users/lucas/Downloads/iShot_2023-03-25_13.52.27.png"
        pixmap = QPixmap(filename)  # 按指定路径找到图片
        self.lane_img.setMaximumSize(600, 400)
        self.lane_img.setMinimumSize(300, 200)
        self.lane_img.setScaledContents(True)  # 让图片自适应label大小
        self.lane_img.setPixmap(pixmap)  # 在label上显示图片

        self.gaze_img = QLabel(self)
        filename = "/Users/lucas/Downloads/iShot_2023-03-25_13.52.27.png"
        pixmap = QPixmap(filename)  # 按指定路径找到图片
        self.gaze_img.setMaximumSize(600, 400)
        self.gaze_img.setMinimumSize(300, 200)
        self.gaze_img.setScaledContents(True)  # 让图片自适应label大小
        self.gaze_img.setPixmap(pixmap)  # 在label上显示图片

        vbox = QVBoxLayout()
        vbox.addWidget(lane_text)
        # vbox.addStretch(1)
        vbox.addWidget(self.lane_img)
        vbox.addStretch(0)

        vvbox = QVBoxLayout()
        vvbox.addWidget(gaze_text)
        # vvbox.addStretch(1)
        vvbox.addWidget(self.gaze_img)
        vvbox.addStretch(0)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(vvbox)

        self.setLayout(hbox)
        # self.setGeometry(0, 0, self.screenwidth, self.screenheight)
        self.setWindowTitle('Driving Distraction Detection System')

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

        self.outerThread = OuterVideoThread()
        self.outerThread.lane_img_change_signal.connect(self.update_lane_image)
        self.outerThread.start()

        self.show()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.gaze_img.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_lane_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.lane_img.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)


def main():
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
