import sys
from PyQt5.QtWidgets import QMainWindow
from ffmpeg_compositor.views.gen.mainview_ui import Ui_MainView


class MainView(QMainWindow, Ui_MainView):
    def __init__(self):
        super(MainView, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
