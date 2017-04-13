import sys
from PyQt5.QtWidgets import QWidget
from ffmpeg_compositor.views.gen.graphview_ui import Ui_GraphView


class GraphView(QWidget, Ui_GraphView):
    def __init__(self):
        super(GraphView, self).__init__()
        self.setupUi(self)
