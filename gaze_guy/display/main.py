import sys
from PyQt6.QtWidgets import QApplication

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
    