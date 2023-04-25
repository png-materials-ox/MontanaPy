from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6 import QtCore
from PySide6.QtGui import QDoubleValidator, QIntValidator
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

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setObjectName("graphWidget")
        self.graphWidget.setStyleSheet(style)
        self.resize(1000, 600)

        # create a linear gradient for the background color
        grad = GUICore._gradient_plot_backround(self.graphWidget)

        # set the background brush of the plot widget to the gradient
        self.graphWidget.setBackgroundBrush(grad)
        self.setCentralWidget(self.graphWidget)

        # Setup the plot
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        self.sample_time = 0.01
        self.window_size = 20    # for averaging
        self.ave_x = self.x[1:]
        self.rolling_ave = [(self.y[i] - self.y[i-1] / 2) for i in range(1, len(self.y))]

        pen = pg.mkPen(color='#ffa02f', width=4)
        self.data_scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=7, color='#ffa02f'), symbol='o', size=3)
        self.data_scatter.setOpacity(0.2)
        self.ave_line = self.graphWidget.plot(self.rolling_ave, pen=pen)

        self.graphWidget.addItem(self.data_scatter)
        self.graphWidget.addItem(self.ave_line)

        self.textItem = pg.TextItem(anchor=(0, 2))
        # self.graphWidget.addItem(self.textItem)

        # Set the position of the TextItem
        # self.textItem.setPos(0, 0)

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

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        start_btn = QPushButton("Start")
        start_btn.setObjectName("Start")
        stop_btn = QPushButton("Stop")
        stop_btn.setObjectName("Stop")
        self.ave_label = QLabel()
        self.ave_label.setText(str(self.rolling_ave[-1]))

        # Create the three form inputs and their labels
        label_ms, input_ms = GUICore._create_label("Dwell time (ms)", "int")
        label_winsize, input_winsize = GUICore._create_label("Average Range", "int")
        label_3, input_3 = GUICore._create_label("", "int")

        layout.addWidget(start_btn, 0, 0)
        layout.addWidget(stop_btn, 0, 1)
        layout.addWidget(self.ave_label, 0, 5)

        layout.addWidget(label_ms, 1, 0)
        layout.addWidget(input_ms, 1, 1)
        layout.addWidget(label_winsize, 1, 2)
        layout.addWidget(input_winsize, 1, 3)
        layout.addWidget(label_3, 1, 5)

        layout.addWidget(self.graphWidget, 2, 0, 2, 6)

        self.setCentralWidget(widget)

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

        self.ave_label.setText(str(self.rolling_ave[-1]))

    def _moving_ave(self, window_size=5):
        i = 0
        moving_averages = []
        while i < len(self.y) - window_size + 1:
            window = self.y[i: i + window_size]
            window_average = round(np.sum(window) / window_size, 2)
            moving_averages.append(window_average)
            i += 1
        return moving_averages

