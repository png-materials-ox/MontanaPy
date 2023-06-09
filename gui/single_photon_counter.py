from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
)
from PySide6 import QtCore
import pyqtgraph as pg

import os
from random import randint
import numpy as np

from hardware.nidaq import DAQ
from gui.core import GUICore


class SPC(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(SPC, self).__init__(*args, **kwargs)

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\single_photon_counter.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        core = SPCCore(style=style)
        self.spc_components = SPCGuiComponents()

        self.resize(1000, 600)

        self.spc_plot_widget = core.spc_plot_widget
        self.textItem = pg.TextItem(anchor=(0, 2))

        # # Attach timer for updating the SPC plot, connecting to update function
        self.timer = core.timer
        self.timer.start()

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        layout.addWidget(core.spc_components.label_ms, 0, 0)
        layout.addWidget(core.spc_components.input_ms, 0, 1)
        layout.addWidget(core.spc_components.label_winsize, 0, 2)
        layout.addWidget(core.spc_components.input_winsize, 0, 3)
        layout.addWidget(core.spc_components.label_3, 0, 5)

        layout.addWidget(self.spc_plot_widget, 1, 0, 2, 6)

        self.setCentralWidget(widget)
        self.setLayout(layout)

class SPCCore(GUICore):
    def __init__(self, style=None):
        super().__init__()
        self.spc_components = SPCGuiComponents()
        plotting = Plotting(style)
        self.spc_plot_widget = plotting.spc_plot_widget

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

        # Attach timer for updating the SPC plot, connecting to update function
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

        # Connect a signal to input1 to store its text as a variable
        self.spc_components.input_ms.returnPressed.connect(lambda:
                                    self.store_sample_time(self.spc_components.input_ms.text()))
        self.spc_components.input_winsize.returnPressed.connect(lambda:
                                    self.store_window_size(self.spc_components.input_winsize.text()))

        self.ave_label = QLabel()
        self.ave_label.setText(str(self.rolling_ave[-1]))

    def store_sample_time(self, text):
        '''

        :param text:
        :return:
        '''
        self.sample_time = float(text)/1000
        print("Input 1:", self.sample_time)
        self.logging.info("Sample time set to {:} ms".format(self.sample_time*1000))

    def store_window_size(self, text):
        '''

        :param text:
        :return:
        '''
        self.window_size = int(text)
        print("Input 2:", self.window_size)
        self.logging.info("Average window size set to {:f}".format(self.window_size))

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

class SPCGuiComponents(GUICore):
    '''

    '''
    def __init__(self):
        '''

        '''
        super().__init__()

        # self.start_btn = super()._create_button('Start', None)
        # self.stop_btn = super()._create_button('Stop', None)

        # Create the three form inputs and their labels
        self.label_ms, self.input_ms = GUICore._create_label("Dwell time (ms)", "int")
        self.label_winsize, self.input_winsize = GUICore._create_label("Average Range", "int")
        self.label_3, self.input_3 = GUICore._create_label("", "int")


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