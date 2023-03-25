import sys
import pyqtgraph as pg
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout)


# Image View class
class ImageView(pg.ImageView):

    # constructor which inherit original
    # ImageView
    def __init__(self, *args, **kwargs):
        pg.ImageView.__init__(self, *args, **kwargs)


class FinalWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.screenwidth = None
        self.screenheight = None
        self.screenRect = None
        self.init_ui()

    def init_ui(self):
        # fit screen
        self.screenRect = QApplication.primaryScreen().geometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()

        lane_text = QLabel("Lane Detection")
        gaze_text = QLabel("Gaze Estimation")

        lane_img = QLabel(self)
        filename = "/Users/lucas/Downloads/iShot_2023-03-25_13.52.27.png"
        pixmap = QPixmap(filename)  # 按指定路径找到图片
        lane_img.setMaximumSize(600, 400)
        lane_img.setMinimumSize(300, 200)
        lane_img.setScaledContents(True)  # 让图片自适应label大小
        lane_img.setPixmap(pixmap)  # 在label上显示图片

        gaze_img = QLabel(self)
        filename = "/Users/lucas/Downloads/iShot_2023-03-25_13.52.27.png"
        pixmap = QPixmap(filename)  # 按指定路径找到图片
        gaze_img.setMaximumSize(600, 400)
        gaze_img.setMinimumSize(300, 200)
        gaze_img.setScaledContents(True)  # 让图片自适应label大小
        gaze_img.setPixmap(pixmap)  # 在label上显示图片

        vbox = QVBoxLayout()
        vbox.addWidget(lane_text)
        # vbox.addStretch(1)
        vbox.addWidget(lane_img)
        vbox.addStretch(0)

        vvbox = QVBoxLayout()
        vvbox.addWidget(gaze_text)
        # vvbox.addStretch(1)
        vvbox.addWidget(gaze_img)
        vvbox.addStretch(0)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(vvbox)

        self.setLayout(hbox)
        # self.setGeometry(0, 0, self.screenwidth, self.screenheight)
        self.setWindowTitle('Driving Distraction Detection System')
        self.show()


def main():
    app = QApplication(sys.argv)
    final_win = FinalWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
