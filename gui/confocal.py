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
from gui.fast_steering_mirror import FSMGuiComponents
from gui.single_photon_counter import SPC, SPCGuiComponents
from gui.single_photon_counter import Plotting as SPCPlotting


class Confocal(GUICore):
    def __init__(self):
        super().__init__()
        spc = SPC()

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
        self.spc_plot_widget = spc_plotting.spc_plot_widget
        self.fsm_plot_widget = plotting.fsm_plot_widget
        self.tst_plot_widget = plotting.tst_plot_widget          # Test plot widget

        # # < iclass ="fa-regular fa-play" style="color: #ffaa00;" > < /i >
        # icon = qta.icon("fa5s.play")
        # button = QPushButton(icon, "Home")



        # Setup the plot
        # First generate some randon data to initially populate the plot
        # TODO: limit the number of random points - currently too many
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        self.sample_time = 0.01  # Number of samples per second
        self.window_size = 20    # Size of window for averaging
        self.ave_x = self.x[1:]  # Initialise averaging
        self.rolling_ave = [(self.y[i] - self.y[i-1] / 2) for i in range(1, len(self.y))]

        pen = pg.mkPen(color='#ffa02f', width=4)
        self.data_scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=7, color='#ffa02f'),
                                               symbol='o', size=3)
        self.data_scatter.setOpacity(0.2)
        self.ave_line = self.spc_plot_widget.plot(self.rolling_ave, pen=pen)  # Average line of scatter pts

        self.spc_plot_widget.addItem(self.data_scatter)
        self.spc_plot_widget.addItem(self.ave_line)

        self.textItem = pg.TextItem(anchor=(0, 2))

        # Attach timer for updating the SPC plot, connecting to update function
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.start_btn = self.spc_components.start_btn
        self.stop_btn = self.spc_components.stop_btn
        self.ave_label = QLabel()
        self.ave_label.setText(str(self.rolling_ave[-1]))

        qb = QHBoxLayout()
        # qb.addWidget(self.spc_components.label_ms)
        qb.addWidget(self.spc_components.input_ms)
        qb.addWidget(self.spc_components.label_winsize)
        qb.addWidget(self.spc_components.input_winsize)



        grid_layout = QGridLayout()
        grid_layout.addWidget(button, 0, 0)
        grid_layout.addLayout(qb, 0, 3)
        grid_layout.addWidget(self.tst_plot_widget, 1, 0, 2, 2)
        grid_layout.addWidget(self.spc_plot_widget, 1, 2, 2, 2)
        grid_layout.addLayout(self.fsm_components.label_box, 3, 3)
        grid_layout.addLayout(self.fsm_components.button_box, 4, 3, 1, 2)
        grid_layout.addLayout(self.fsm_components.hbox, 5, 3, 1, 2)
        grid_layout.addWidget(self.fsm_plot_widget, 6, 3, 2, 2)
        self.setLayout(grid_layout)  # Set the layout for the widget

        self.show()

        # Connect a signal to input1 to store its text as a variable
        self.spc_components.input_ms.returnPressed.connect(lambda:
                                                           self.store_sample_time(self.spc_components.input_ms.text()))
        self.spc_components.input_winsize.returnPressed.connect(lambda:
                                                                self.store_window_size(
                                                                    self.spc_components.input_winsize.text()))

        # self.setLayout(layout)

    def store_sample_time(self, text):
        '''

        :param text:
        :return:
        '''
        self.sample_time = float(text) / 1000
        print("Input 1:", self.sample_time)

    def store_window_size(self, text):
        '''

        :param text:
        :return:
        '''
        self.window_size = int(text)
        print("Input 2:", self.window_size)

    def update_plot_data(self):
        '''

        :return:
        '''

        self.x = self.x[1:]  # Remove the first y element.

        self.y = self.y[1:]  # Remove the first
        self.ave_x = self.ave_x[1:]
        self.rolling_ave = self.rolling_ave[1:]
        time_total = 0

        daq = DAQ()
        p = daq.counter(self.sample_time)

        time_total = self.x[-1] + 1

        self.x.append(time_total)
        self.y.append(p)
        self.data_scatter.setData(self.x, self.y)

        self.ave_x.append(self.x[-self.window_size])
        self.rolling_ave.append(sum(self.y[-self.window_size:]) / self.window_size)

        self.ave_line.setData(self.ave_x, self.rolling_ave)

        self.ave_label.setText(str(self.rolling_ave[-1]))

    def _moving_ave(self, window_size=5):
        '''

        :param window_size:
        :return:
        '''
        i = 0
        moving_averages = []
        while i < len(self.y) - window_size + 1:
            window = self.y[i: i + window_size]
            window_average = round(np.sum(window) / window_size, 2)
            moving_averages.append(window_average)
            i += 1
        return moving_averages

class Plotting(GUICore):
    def __init__(self, style):
        super().__init__()

        self.fsm_plot_widget = pg.PlotWidget()
        grad = super()._gradient_plot_backround(self.fsm_plot_widget)  # color gradient
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
