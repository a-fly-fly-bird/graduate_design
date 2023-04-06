import sys
import time
import cv2
import numpy as np

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout

from gaze_guy.display.qthreads import MediaPipeHeadPoseEstimationThread, DLGazeEstimationThread
from gaze_guy.ptgaze.demo import Demo

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.threads = {}
        self.units = {}
        self.screenHeight = 0
        self.screenWidth = 0
        self.initUI()
    
    def initUI(self):
        screenRect = QApplication.primaryScreen().geometry()
        self.screenHeight = screenRect.height() # 900
        self.screenWidth = screenRect.width() # 1440

        label1 = QLabel("算法一")
        lebel2 = QLabel("算法二")
        img1 = self.setDefaultImgLabel()
        img2 = self.setDefaultImgLabel()
        self.units['lane'] = (label1, img1)
        self.units['gaze'] = (lebel2, img2)
        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addWidget(self.units['lane'][0])
        vbox1.addWidget(self.units['lane'][1])
        vbox1.addStretch(1)
        vbox2 = QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.units['gaze'][0])
        vbox2.addWidget(self.units['gaze'][1])
        vbox2.addStretch(1)
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addLayout(vbox1)
        hbox1.addStretch(1)
        hbox1.addLayout(vbox2)
        hbox1.addStretch(1)
        self.setLayout(hbox1)
        self.setGeometry(self.screenWidth // 6, self.screenHeight // 6, self.screenWidth // 6 * 4, self.screenHeight // 6 * 4)
        self.setWindowTitle('驾驶分心检测系统')

        self.threads['t1'] = MediaPipeHeadPoseEstimationThread()
        self.threads['t2'] = None
        self.threads['t1'].headPoseEstimationSignal.connect(self.update_lane_image)

    def startDLGazeEstimationThread(self, config):
        demo = Demo(config)
        self.threads['t2'] = demo
        self.threads['t2'].gazeEstimationSignal.connect(self.update_gaze_image)
        self.startEvent()

    def startEvent(self):
        for thread in self.threads.values():
            thread.start()
    
    def closeEvent(self, event):
        for thread in self.threads.values():
            thread.stop_thread()
        event.accept()

    def setDefaultImgLabel(self):
        label = QLabel(self)
        filename = '../assets/default.jpg'
        pixmap = QPixmap(filename)  # 按指定路径找到图片
        label.setMaximumSize(self.screenHeight, self.screenHeight)
        label.setMinimumSize(self.screenHeight // 8, self.screenHeight // 8)
        label.setScaledContents(True)  # 让图片自适应label大小
        label.setPixmap(pixmap)  # 在label上显示图片
        return label

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.screenWidth // 3, self.screenWidth // 3, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @pyqtSlot(np.ndarray)
    def update_lane_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.units['lane'][1].setPixmap(qt_img)
    
    @pyqtSlot(np.ndarray)
    def update_gaze_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.units['gaze'][1].setPixmap(qt_img)
