from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
    QPushButton,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLabel,
)
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
import os

from gui.core import GUICore
from gui.fast_steering_mirror import FSMGuiComponents


class Confocal(GUICore):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\confocal.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)

        self.fsm_components = FSMGuiComponents()

        ########################################
        #### Create a grid layout container ####
        ########################################
        grid_layout = QGridLayout()
        # grid_layout.addLayout(label_box, 0, 0)
        # grid_layout.addLayout(self.button_box, 1, 0, 1, 2)
        # grid_layout.addLayout(hbox, 2, 0, 1, 2)
        # grid_layout.addWidget(self.plot_widget, 3, 0, 2, 2)