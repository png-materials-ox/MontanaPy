from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPushButton
)
from PySide6.QtGui import QLinearGradient
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
from contextlib import contextmanager

class GUICore(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    @staticmethod
    def _create_button(name, layout):
        button = QPushButton(name)
        button.setObjectName(name)
        layout.addWidget(button)
        return button

    @staticmethod
    def _gradient_plot_backround(plot_widget):
        grad = QLinearGradient(0, 0, 0, plot_widget.height())
        grad.setColorAt(0, pg.mkColor('#565656'))
        grad.setColorAt(0.1, pg.mkColor('#525252'))
        grad.setColorAt(0.5, pg.mkColor('#4e4e4e'))
        grad.setColorAt(0.9, pg.mkColor('#4a4a4a'))
        grad.setColorAt(1, pg.mkColor('#464646'))
        return grad

    @staticmethod
    def _open_window(self, obj, title):
        self.window = obj
        self.window.setWindowTitle(title)
        self.window.show()
        self.window.setParent(None)

    @contextmanager
    def qtimer(self, func, interval):
        try:
            timer = QTimer()
            timer.timeout.connect(func)
            timer.start(interval)  # interval is in milliseconds
            yield
        finally:
            timer.stop()