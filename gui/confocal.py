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
import qtawesome as qta
import os
from random import randint
import numpy as np
from hardware.nidaq import DAQ

from gui.core import GUICore
from gui.fast_steering_mirror import FSMCore, FSMGuiComponents
from gui.single_photon_counter import SPCCore, SPCGuiComponents
from gui.single_photon_counter import Plotting as SPCPlotting


class Confocal(GUICore):
    def __init__(self):
        super().__init__()
        spc = SPCCore()
        fsm = FSMCore()

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\confocal.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)

        self.fsm_components = FSMGuiComponents(xsteps=None, ysteps=None, roi=None, dwell_ms=None)
        self.spc_components = SPCGuiComponents()

        spc_plotting = SPCPlotting(style)
        plotting = Plotting(style)
        self.tst_plot_widget = plotting.tst_plot_widget          # Test plot widget

        self.spc_plot_widget = spc.spc_plot_widget
        self.textItem = pg.TextItem(anchor=(0, 2))

        # # Attach timer for updating the SPC plot, connecting to update function
        self.spc_timer = spc.timer
        self.spc_timer.start()

        self.fsm_plot_widget = fsm.fsm_plot_widget
        self.fsm_timer = fsm.timer
        self.fsm_timer.start(10)  # interval is in milliseconds

        qb = QHBoxLayout()
        qb.addWidget(spc.spc_components.label_ms)
        qb.addWidget(spc.spc_components.input_ms)
        qb.addWidget(spc.spc_components.label_winsize)
        qb.addWidget(spc.spc_components.input_winsize)

        grid_layout = QGridLayout()
        # grid_layout.addWidget(button, 0, 0)
        grid_layout.addLayout(qb, 0, 3)
        grid_layout.addWidget(self.tst_plot_widget, 1, 0, 2, 2)
        grid_layout.addWidget(self.spc_plot_widget, 1, 2, 2, 2)
        grid_layout.addLayout(fsm.label_box, 4, 3)
        # grid_layout.addLayout(fsm.button_box, 4, 3, 1, 2)
        grid_layout.addLayout(fsm.hbox, 5, 3, 1, 2)
        grid_layout.addWidget(self.fsm_plot_widget, 6, 3, 2, 2)
        self.setLayout(grid_layout)  # Set the layout for the widget

        self.show()


class Plotting(GUICore):
    def __init__(self, style):
        super().__init__()

        # Test plot widget
        self.tst_plot_widget = pg.PlotWidget()
        grad = super()._gradient_plot_backround(self.tst_plot_widget)  # color gradient
        self.tst_plot_widget.setBackgroundBrush(grad)  # set the background brush of the plot widget to the gradient