import sys
from PyQt5.QtWidgets import QWidget
from ffmpeg_compositor.views.gen.filtersview_ui import Ui_FiltersView


class FiltersView(QWidget, Ui_FiltersView):
    def __init__(self):
        super(FiltersView, self).__init__()
        self.setupUi(self)
