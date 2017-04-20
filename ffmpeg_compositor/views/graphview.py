from PyQt5.QtWidgets import QWidget, QGraphicsScene
from ffmpeg_compositor.views.gen.graphview_ui import Ui_GraphView

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PyQt5.QtWidgets import QGraphicsSceneMouseEvent


class GraphView(QWidget, Ui_GraphView):
    def __init__(self):
        super(GraphView, self).__init__()
        self.setupUi(self)
        self.scene = GraphScene()
        self.gridView.setScene(self.scene)


class GraphScene(QGraphicsScene):
    def __init__(self):
        super(GraphScene, self).__init__()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        #print(event.scenePos())
        pass
