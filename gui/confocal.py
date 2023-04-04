from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QApplication,
    QVBoxLayout,
    QLabel,
)
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
import sys
import numpy as np
import os
from random import randint
import time
import nidaqmx

class Confocal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\confocal.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        layout = QVBoxLayout()

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)

        # # Add the plot generated after program execution to the layout
        # self.plot1 = pg.PlotWidget()
        # self.plot1.plot(np.random.normal(size=100))
        # layout.addWidget(self.plot1)

        # Add the live data plot to the layout
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setStyleSheet(style)
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        # self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        # self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen, color='green')
        self.data_line = pg.ScatterPlotItem(pen=pg.mkPen(width=7, color='green'), symbol='o', size=3)
        self.graphWidget.addItem(self.data_line)
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot2)
        self.timer.start()

        # # Add the plot generated after program execution to the layout
        # self.plot3 = pg.PlotWidget()
        # self.plot3.plot(np.random.normal(size=100))
        # layout.addWidget(self.plot3)

        # Set the layout for the main window
        self.setLayout(layout)

    def update_plot2(self):
        # # Update the live data plot with new data
        # x = np.linspace(0, 10, 100)
        # y = np.random.rand(100)
        # self.plot2.plot(x, y)

        while True:
            try:
                self.x = self.x[1:]  # Remove the first y element.
                # self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

                self.y = self.y[1:]  # Remove the first
                # self.y.append( randint(0,100))  # Add a new random value.
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
                    self.data_line.setData(self.x, self.y)  # Update the data.

            except nidaqmx.DaqError as e:
                print("An error occurred:", e)

            except Exception as e:
                print("An unexpected error occurred:", e)

            finally:
                task.close()