from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QTabWidget,
    QPushButton,
    QLineEdit
)
from PySide6.QtGui import QLinearGradient, QDoubleValidator, QIntValidator
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg

import os
from contextlib import contextmanager
import logging

class GUICore(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # conf_path = os.path.join(os.getcwd() + "\\config\\config.json")
        #
        # with self._open_config(conf_path) as config:
        #     self.daq = config["hardware"]["nicard"]  # Daq device ID

        logging.basicConfig(filename='log/log.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')
        self.logging = logging.getLogger("log/log.log")

    @staticmethod
    def _create_button(name, layout):
        button = QPushButton(name)
        button.setObjectName(name)
        layout.addWidget(button)
        return button

    @staticmethod
    def _create_label(name, validator, placeholder="Enter your text here"):
        label = QLabel(name)
        input = QLineEdit()
        input.setPlaceholderText(placeholder)
        if validator == 'int':
            input.setValidator(QIntValidator())
        elif validator == 'double':
            input.setValidator(QDoubleValidator())
        return (label, input)

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
        logging.info(f'{title} Opened')

    @contextmanager
    def qtimer(self, func, interval):
        try:
            timer = QTimer()
            timer.timeout.connect(func)
            timer.start(interval)  # interval is in milliseconds
            yield
        finally:
            timer.stop()
