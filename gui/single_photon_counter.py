from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QLinearGradient
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import time
import nidaqmx

class SPC(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(SPC, self).__init__(*args, **kwargs)

        style = """
            QWidget {
                background-color: #f0f0f0;
            }

            QFrame {
                background-color: white;
                border: 1px solid #c0c0c0;
            }

            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #404040;
            }

            QwtPlotCanvas {
                background-color: white;
            }

            QwtPlotGrid {
                pen: #c0c0c0;
            }

            QwtPlotCurve {
                pen: #4040ff;
            }
            """
        # plot.setStyleSheet(style)

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
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        # self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        # self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen, color='green')
        self.data_scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=7, color='#ffa02f'), symbol='o', size=3)
        self.graphWidget.addItem(self.data_scatter)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
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