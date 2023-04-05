from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QLinearGradient, QDoubleValidator, QIntValidator
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import time

from hardware.nidaq import DAQ

import pandas as pd
import numpy as np

class SPC(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(SPC, self).__init__(*args, **kwargs)

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\single_photon_counter.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setStyleSheet(style)
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

        self.sample_time = 0.01
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

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        widget.setLayout(layout)

        # ms_label = QtWidgets.QLabel("Sample Time (ms)")
        # ms_form = QtWidgets.QLineEdit("Sample Time (ms)")

        # Create the three form inputs and their labels
        label_ms = QtWidgets.QLabel("Sample time (ms):")
        input_ms = QtWidgets.QLineEdit()
        input_ms.setValidator(QDoubleValidator())
        label_winsize = QtWidgets.QLabel("Average Range:")
        input_winsize = QtWidgets.QLineEdit()
        input_winsize.setValidator(QIntValidator())
        label3 = QtWidgets.QLabel("")

        layout.addWidget(label_ms, 0, 0)
        layout.addWidget(input_ms, 0, 1)
        layout.addWidget(label_winsize, 0, 2)
        layout.addWidget(input_winsize, 0, 3)
        layout.addWidget(label3, 0, 5)

        layout.addWidget(self.graphWidget, 1, 0, 1, 6)

        self.setCentralWidget(widget)

        # text_item = pg.TextItem(anchor=(1, 1))
        # self.graph_widget.addItem(text_item)

        # Connect a signal to input1 to store its text as a variable
        input_ms.returnPressed.connect(lambda: self.store_sample_time(input_ms.text()))
        input_winsize.returnPressed.connect(lambda: self.store_window_size(input_winsize.text()))

        self.setLayout(layout)

    def store_sample_time(self, text):
        self.sample_time = float(text)/1000
        print("Input 1:", self.sample_time)

    def store_window_size(self, text):
        self.window_size = int(text)
        print("Input 2:", self.window_size)

    def update_plot_data(self):

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

        print(self.rolling_ave[-1])

    def _moving_ave(self, window_size=5):
        i = 0
        moving_averages = []
        while i < len(self.y) - window_size + 1:
            window = self.y[i: i + window_size]
            window_average = round(np.sum(window) / window_size, 2)
            moving_averages.append(window_average)
            i += 1
        return moving_averages
