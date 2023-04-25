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
from core import Core

class GUICore(QWidget):
    def __init__(self, parent=None):
        '''
        Initializes the GUICore class.

        :param parent: (QWidget) The parent widget. Defaults to None.
        '''
        super().__init__(parent)

        conf_path = os.path.join(os.getcwd() + "\\config\\config.json")

        with Core()._open_config(conf_path) as config:
            self.logfile = config["debug"]["logfile"]

        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')
        self.logging = logging.getLogger(self.logfile)

    @staticmethod
    def _create_button(name, layout):
        '''
        Creates a QPushButton with the given name and adds it to the layout if one is provided.

        :param name: (str) The name of the button.
        :param layout: (QLayout) The layout to add the button to.
        :return: (QPushButton) The newly created button.
        '''
        button = QPushButton(name)
        button.setObjectName(name)
        if layout:
            layout.addWidget(button)
        return button

    @staticmethod
    def _create_label(name, validator, placeholder="Enter your text here"):
        '''
        Creates a QLabel and a QLineEdit with the given name and validator, and sets the
        placeholder text.

        :param name: (str) The name of the label.
        :param validator: (str) The type of validator to use for the QLineEdit. Should be either '
                           int' or 'double'.
        :param placeholder: (str) The text to display as a placeholder in the QLineEdit.
                            Defaults to "Enter your text here".
        :return: (tuple) A tuple containing the QLabel and QLineEdit objects.
        '''
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
        '''
        Creates a QLinearGradient to use as a background for a Pyqtgraph plot widget.

        :param plot_widget: (Pyqtgraph PlotWidget) The plot widget to set the background for.
        :return: (QLinearGradient) The newly created gradient object.
        '''
        grad = QLinearGradient(0, 0, 0, plot_widget.height())
        grad.setColorAt(0, pg.mkColor('#565656'))
        grad.setColorAt(0.1, pg.mkColor('#525252'))
        grad.setColorAt(0.5, pg.mkColor('#4e4e4e'))
        grad.setColorAt(0.9, pg.mkColor('#4a4a4a'))
        grad.setColorAt(1, pg.mkColor('#464646'))
        return grad

    @staticmethod
    def _open_window(self, obj, title):
        '''
        Opens a new window with the given title.

        :param obj: (QWidget) The widget to use as the window.
        :param title: (str) The title to set for the window.
        '''
        self.window = obj
        self.window.setWindowTitle(title)
        self.window.show()
        self.window.setParent(None)
        logging.info(f'{title} Opened')

    @contextmanager
    def qtimer(self, func, interval):
        '''

        :param func:
        :param interval:
        :return:
        '''
        try:
            timer = QTimer()
            timer.timeout.connect(func)
            timer.start(interval)  # interval is in milliseconds
            yield
        finally:
            timer.stop()
