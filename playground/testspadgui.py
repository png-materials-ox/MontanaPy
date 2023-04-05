from PySide6 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import time
import nidaqmx

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

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
        self.graphWidget.setStyleSheet(style)
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        # self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        # self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen, color='green')
        self.data_line = pg.ScatterPlotItem(pen=pg.mkPen(width=7, color='green'), symbol='o', size=3)
        self.graphWidget.addItem(self.data_line)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

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


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())