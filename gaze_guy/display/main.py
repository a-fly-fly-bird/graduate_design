import sys
import time
import cv2
import numpy as np

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout

from gaze_guy.display.main_window import App
from gaze_guy.display.parse import my_parse

def main():
    config = my_parse()
    app = QApplication(sys.argv)
    a = App()
    a.startDLGazeEstimationThread(config)
    a.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()