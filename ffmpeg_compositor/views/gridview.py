# Inspired by https://github.com/cb109/qtnodes/blob/develop/qtnodes/view.py

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QLineF, QPoint, QRect, QRectF
from PyQt5.QtGui import QColor, QBrush, QPen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PyQt5.QtGui import QPainter, QMouseEvent, QKeyEvent, QWheelEvent, QTransform
    from PyQt5.QtCore import QRectF, QRect


class GridView(QGraphicsView):
    #GRID_SPACING = 50
    GRID_SPACING = 1000
    ALTERNATE_MODE_KEY = Qt.Key_Control
    LINE_COLOR = QColor(160, 160, 160)
    LINE_ORIGIN_COLOR = QColor(120, 120, 120)
    FILL_COLOR = QColor(180, 180, 180)

    MAX_FACTOR = 1.5
    MIN_FACTOR = 0.5
    FACTOR_STEP = 0.1

    _alternate_mode = False
    _panning = False
    factor = 1.0

    def __init__(self, parent):
        super(GridView, self).__init__(parent)

        self.panning = False

        self.panningMult = 1.0
        self.prevPos = QPoint(0, 0)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    @property
    def panning(self):
        return self._panning

    @panning.setter
    def panning(self, value: bool):
        self._panning = value
        if self._panning:
            self.setDragMode(QGraphicsView.NoDrag)
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        self.update_cursor()

    @property
    def alternate_mode(self):
        return self._alternate_mode

    @alternate_mode.setter
    def alternate_mode(self, value: bool):
        self._alternate_mode = value
        self.update_cursor()

    def drawBackground(self, painter: 'QPainter', floating_rect: 'QRectF'):
        rect = floating_rect.toAlignedRect()  # type: 'QRect'

        painter.setBrush(QBrush(GridView.FILL_COLOR))
        line_pen = QPen(GridView.LINE_COLOR)
        line_pen.setWidth(0)
        line_pen.setCosmetic(True)
        line_origin_pen = QPen(GridView.LINE_ORIGIN_COLOR)
        line_origin_pen.setWidth(1)
        line_origin_pen.setCosmetic(True)

        painter.drawRect(rect)

        left = floating_rect.left()
        right = floating_rect.right()
        top = floating_rect.top()
        bottom = floating_rect.bottom()

        for x in range(int(left * 100.0), int(right * 100.0)):
            if x % GridView.GRID_SPACING == 0:
                line = QLineF(x / 100.0, floating_rect.top(), x / 100.0, floating_rect.bottom())
                if x == 0:
                    painter.setPen(line_origin_pen)
                else:
                    painter.setPen(line_pen)
                painter.drawLine(line)

        for y in range(int(top * 100.0), int(bottom * 100.0)):
            if y % GridView.GRID_SPACING == 0:
                line = QLineF(floating_rect.left(), y / 100.0, floating_rect.right(), y / 100.0)
                if y == 0:
                    painter.setPen(line_origin_pen)
                else:
                    painter.setPen(line_pen)
                painter.drawLine(line)

    def keyPressEvent(self, event: 'QKeyEvent'):
        if event.key() == GridView.ALTERNATE_MODE_KEY:
            self.alternate_mode = True

    def keyReleaseEvent(self, event: 'QKeyEvent'):
        if event.key() == GridView.ALTERNATE_MODE_KEY:
            self.alternate_mode = False

    def mousePressEvent(self, event: 'QMouseEvent'):
        if event.button() == Qt.LeftButton:
            if self.alternate_mode:
                self.panning = True
        super(GridView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: 'QMouseEvent'):
        if event.button() == Qt.LeftButton:
            self.panning = False
        super(GridView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: 'QMouseEvent'):
        self.setFocus(Qt.MouseFocusReason)
        if self.panning:
            delta = (self.mapToScene(event.pos()) * self.panningMult -
                     self.mapToScene(self.prevPos) * self.panningMult) * -1.0
            center = QPoint(self.viewport().width() / 2 + delta.x(),
                                   self.viewport().height() / 2 + delta.y())
            newCenter = self.mapToScene(center)
            self.centerOn(newCenter)
            self.prevPos = event.pos()

        super(GridView, self).mouseMoveEvent(event)

    def wheelEvent(self, event: 'QWheelEvent'):
        if self.alternate_mode:
            anchor = self.transformationAnchor()
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            angle = event.angleDelta().y()
            if angle >= 0:
                if self.factor + GridView.FACTOR_STEP >= GridView.MAX_FACTOR:
                    self.factor = GridView.MAX_FACTOR
                else:
                    self.factor += GridView.FACTOR_STEP
            else:
                if self.factor - GridView.FACTOR_STEP <= GridView.MIN_FACTOR:
                    self.factor = GridView.MIN_FACTOR
                else:
                    self.factor -= GridView.FACTOR_STEP
            self.factor = int(self.factor * 100.0) / 100
            self.resetTransform()
            self.scale(self.factor, self.factor)
            self.setTransformationAnchor(anchor)
        super(GridView, self).wheelEvent(event)

    def update_cursor(self):
        if self.panning:
            self.setCursor(Qt.ClosedHandCursor)
        else:
            if self.alternate_mode:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
