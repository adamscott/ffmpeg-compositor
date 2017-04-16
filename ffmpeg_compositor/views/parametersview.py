from PyQt5.QtWidgets import QWidget
from ffmpeg_compositor.views.gen.parametersview_ui import Ui_ParametersView


class ParametersView(QWidget, Ui_ParametersView):
    def __init__(self):
        super(ParametersView, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
