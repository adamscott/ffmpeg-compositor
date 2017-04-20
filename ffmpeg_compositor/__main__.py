import sys
from PyQt5.QtWidgets import QApplication
from ffmpeg_compositor.views.mainview import MainView


def main():
    app = QApplication(sys.argv)
    mv = MainView()
    mv.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
