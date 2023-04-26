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
from gui.single_photon_counter import SPCGuiComponents


class Confocal(GUICore):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\confocal.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)

        self.fsm_components = FSMGuiComponents(xsteps=None, ysteps=None, roi=None, dwell_ms=None)
        self.spc_components = SPCGuiComponents()

        plotting = Plotting(style)
        self.spc_plot_widget = plotting.spc_plot_widget
        self.fsm_plot_widget = plotting.fsm_plot_widget
        self.tst_plot_widget = plotting.tst_plot_widget          # Test plot widget





        





        grid_layout = QGridLayout()
        grid_layout.addWidget(self.tst_plot_widget, 0, 0, 2, 2)
        grid_layout.addWidget(self.spc_plot_widget, 0, 2, 2, 2)
        grid_layout.addLayout(self.fsm_components.label_box, 2, 3)
        grid_layout.addLayout(self.fsm_components.button_box, 3, 3, 1, 2)
        grid_layout.addLayout(self.fsm_components.hbox, 4, 3, 1, 2)
        grid_layout.addWidget(self.fsm_plot_widget, 5, 3, 2, 2)
        self.setLayout(grid_layout)  # Set the layout for the widget

        self.show()

class Plotting(GUICore):
    def __init__(self, style):
        super().__init__()

        self.spc_plot_widget = pg.PlotWidget()
        self.spc_plot_widget.setObjectName("spc_graph")
        self.spc_plot_widget.setStyleSheet(style)
        grad = super()._gradient_plot_backround(self.spc_plot_widget)  # color gradient
        self.spc_plot_widget.setBackgroundBrush(grad)

        ps = PlotStyling(self.spc_plot_widget)
        self.spc_plot_widget.setTitle("Single Photon Counter", **ps.title_style)
        self.spc_plot_widget.setLabel('bottom', "", **ps.x_label_style)
        self.spc_plot_widget.setLabel('left', "Counts/s", **ps.y_label_style)

        self.fsm_plot_widget = pg.PlotWidget()
        self.fsm_plot_widget.setBackgroundBrush(grad)  # set the background brush of the plot widget to the gradient

        # Test plot widget
        self.tst_plot_widget = pg.PlotWidget()
        self.tst_plot_widget.setBackgroundBrush(grad)  # set the background brush of the plot widget to the gradient


class PlotStyling:
    def __init__(self, gw):
        self.title_style = {'color': '#FFFFFF', 'font-size': '24pt', 'font-weight': 'bold'}
        self.x_label_style = {'color': '#FFFFFF', 'font-size': '12pt', 'font-weight': 'bold'}
        self.y_label_style = {'color': '#FFFFFF', 'font-size': '12pt', 'font-weight': 'bold'}

        self.x_axis = gw.getAxis('bottom')
        x_tick_font = pg.QtGui.QFont('Arial', 12, weight=pg.QtGui.QFont.Bold)
        self.x_axis.setTickFont(x_tick_font)
        self.x_axis.setPen(pg.mkPen(color='#FFFFFF'))

        self.y_axis = gw.getAxis('left')
        y_tick_font = pg.QtGui.QFont('Arial', 12, weight=pg.QtGui.QFont.Bold)
        self.y_axis.setTickFont(y_tick_font)
        self.y_axis.setPen(pg.mkPen(color='#FFFFFF'))
