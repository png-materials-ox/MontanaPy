from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QLinearGradient
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import time
import nidaqmx

import pandas as pd
import numpy as np

class SPC(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(SPC, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.resize(1000, 600)

        # create a linear gradient for the background color
        # TODO Put into css style file
        grad = QLinearGradient(0, 0, 0, self.graphWidget.height())
        grad.setColorAt(0, pg.mkColor('#565656'))
        grad.setColorAt(0.1, pg.mkColor('#525252'))
        grad.setColorAt(0.5, pg.mkColor('#4e4e4e'))
        grad.setColorAt(0.9, pg.mkColor('#4a4a4a'))
        grad.setColorAt(1, pg.mkColor('#464646'))

        # set the background brush of the plot widget to the gradient
        self.graphWidget.setBackgroundBrush(grad)
        # self.graphWidget.setStyleSheet(style)
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        self.window_size = 20
        self.ave_x = self.x[1:]
        self.rolling_ave = [(self.y[i] - self.y[i-1] / 2) for i in range(1, len(self.y))]
        # self.rolling_ave = self._moving_ave(window_size=5)

        # self.graphWidget.setBackground('w')

        pen = pg.mkPen(color='#ffa02f', width=4)
        self.data_scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=7, color='#ffa02f'), symbol='o', size=3)
        self.data_scatter.setOpacity(0.2)
        self.ave_line = self.graphWidget.plot(self.rolling_ave, pen=pen)

        self.graphWidget.addItem(self.data_scatter)
        self.graphWidget.addItem(self.ave_line)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # TODO Put all this into css style file
        title_style = {'color': '#FFFFFF', 'font-size': '24pt', 'font-weight': 'bold'}
        self.graphWidget.setTitle("Single Photon Counter", **title_style)

        # set the font size and weight of the x-axis label
        x_label_style = {'color': '#FFFFFF', 'font-size': '12pt', 'font-weight': 'bold'}
        self.graphWidget.setLabel('bottom', "", **x_label_style)

        # set the font size and weight of the y-axis label
        y_label_style = {'color': '#FFFFFF', 'font-size': '12pt', 'font-weight': 'bold'}
        self.graphWidget.setLabel('left', "Counts/s", **y_label_style)

        x_axis = self.graphWidget.getAxis('bottom')
        x_tick_font = pg.QtGui.QFont('Arial', 12, weight=pg.QtGui.QFont.Bold)
        x_axis.setTickFont(x_tick_font)
        x_axis.setPen(pg.mkPen(color='#FFFFFF'))

        y_axis = self.graphWidget.getAxis('left')
        y_tick_font = pg.QtGui.QFont('Arial', 12, weight=pg.QtGui.QFont.Bold)
        y_axis.setTickFont(y_tick_font)
        y_axis.setPen(pg.mkPen(color='#FFFFFF'))

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.

        self.y = self.y[1:]  # Remove the first
        self.ave_x = self.ave_x[1:]
        self.rolling_ave = self.rolling_ave[1:]
        time_total = 0
        with nidaqmx.Task() as task:
            task.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")
            task.ci_channels[0].ci_count_edges_term = "/Dev1/PFI8"

            sample_time = 0.01
            task.start()
            time.sleep(sample_time)
            cnt0 = task.read()
            time.sleep(sample_time)

            cnt1 = task.read()
            task.stop()
            p = (cnt1 - cnt0) * (sample_time) ** -1

            time_total = self.x[-1] + 1

            self.x.append(time_total)
            self.y.append(p)
            self.data_scatter.setData(self.x, self.y)

            self.ave_x.append(self.x[-self.window_size])
            self.rolling_ave.append(sum(self.y[-self.window_size:]) / self.window_size)
            # self.rolling_ave.append(self._moving_ave(window_size=2))
            self.ave_line.setData(self.ave_x, self.rolling_ave)
            # self.ave_line.setData(self.rolling_ave)

    def _moving_ave(self, window_size=5):
        i = 0
        moving_averages = []
        while i < len(self.y) - window_size + 1:
            window = self.y[i: i + window_size]
            window_average = round(np.sum(window) / window_size, 2)
            moving_averages.append(window_average)
            i += 1
        return moving_averages

