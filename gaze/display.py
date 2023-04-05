import sys
import time

import cv2
import numpy as np
from PyQt6.QtCore import pyqtSlot, Qt, QThread
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout

from gaze.video_thread import OuterVideoThread


# 不能跨线程计算FPS，误差太大！
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.screenRect = None
        self.screenwidth = None
        self.screenheight = None

        self.display_height = None
        self.display_width = None

        self.lane_img = None
        self.gaze_img = None

        self.outerThread = None
        self.thread = None
        self.anotherThread: QThread = None

        self.init_ui()

    def setAnotherThread(self, thread1):
        self.anotherThread = thread1

    def init_ui(self):
        # fit screen
        self.screenRect = QApplication.primaryScreen().geometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()
        self.display_width = self.screenwidth // 3
        self.display_height = self.screenheight // 3

        lane_text = QLabel("Lane Detection")
        gaze_text = QLabel("Gaze Estimation")

        self.lane_img = self.setDefaultImgLabel()
        self.gaze_img = self.setDefaultImgLabel()

        vbox1 = QVBoxLayout()
        vbox1.addWidget(lane_text)
        vbox1.addWidget(self.lane_img)
        vbox1.addStretch(0)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(gaze_text)
        vbox2.addWidget(self.gaze_img)
        vbox2.addStretch(0)

        hbox1 = QHBoxLayout()
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.setLayout(hbox1)
        # self.setGeometry(0, 0, self.screenwidth, self.screenheight)
        self.setWindowTitle('Driving Distraction Detection System')

        # create the video capture thread
        # self.thread = VideoThread()
        # connect its signal to the update_image slot
        # self.thread.gaze_img_change_signal.connect(self.update_image)
        # start the thread
        # self.thread.start()

        self.outerThread = OuterVideoThread()
        self.outerThread.lane_img_change_signal.connect(self.update_lane_image)
        self.outerThread.start_time_signal.connect(self.calculate_time)
        self.outerThread.start()

    def setDefaultImgLabel(self):
        label = QLabel(self)
        filename = 'assets/default.jpg'
        pixmap = QPixmap(filename)  # 按指定路径找到图片
        label.setMaximumSize(600, 400)
        label.setMinimumSize(300, 200)
        label.setScaledContents(True)  # 让图片自适应label大小
        label.setPixmap(pixmap)  # 在label上显示图片
        return label

    def closeEvent(self, event):
        # self.thread.stop()
        self.outerThread.stop()
        self.anotherThread.stop_la()
        event.accept()

    @pyqtSlot(float)
    def calculate_time(self, start_time):
        end_time = time.time()
        gap = end_time - start_time
        print(f'FPS: {1 / gap}')

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
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)


def main():
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
