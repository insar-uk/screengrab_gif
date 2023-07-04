from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import QWidget, QMainWindow


QLeftMouseButton = Qt.LeftButton  # type: ignore


class ScreenExtentGrabber(QWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__()

        self.mouse_pressed = False
        self.capture_extent = (QPoint(), QPoint())

        # If a parent is not provided, throw an error
        if not parent:
            raise ValueError('Parent window is required to initialize ScreenExtentGrabber')

        self.main_window_handle = parent

        self.setMouseTracking(True)  # Receive mouse move events even without clicking

    def set_main_window_handle(self, main_window: QMainWindow):
        self.main_window_handle = main_window

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == QLeftMouseButton:
            self.mouse_pressed = True
            self.capture_extent = (event.globalPos(), event.globalPos())  # Start position of the capture extent

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.mouse_pressed:
            self.capture_extent = (self.capture_extent[0], event.globalPos())  # Update the end position of the capture extent
            self.update()  # Request repaint to show the extent

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:  # type: ignore
            self.mouse_pressed = False
            self.capture_extent = (self.capture_extent[0], event.globalPos())  # Finalize the end position of the capture extent
            self.update()  # Request repaint to show the final extent

            # Access MainWindow instance
            self.main_window_handle.capture_extent_updated(self.capture_extent_to_rect())

            # Hide the screen extent grabber widget
            self.hide()

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)

        if bool(self.capture_extent):
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.DashLine))  # type: ignore
            painter.setBrush(QBrush(QColor(255, 0, 0, 30)))
            painter.drawRect(self.capture_extent_to_rect().translated(-self.pos()))

    def capture_extent_to_rect(self):
        if bool(self.capture_extent):
            # Get the offset of the widget from the top left corner of the screen
            offset = self.main_window_handle.pos()
            print(offset)
            start_pos, end_pos = self.capture_extent
            if not (bool(end_pos) & bool(start_pos)):
                print('Capture extent is not complete or out of bounds')
                return QRect(0, 0, 0, 0)
            left = min(start_pos.x(), end_pos.x())
            top = min(start_pos.y(), end_pos.y())
            width = abs(start_pos.x() - end_pos.x())
            height = abs(start_pos.y() - end_pos.y())
            return QRect(left, top, width, height)
        return QRect()
