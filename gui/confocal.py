from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QApplication,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
import sys
import numpy as np

import time
import nidaqmx

class Confocal(QWidget):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open('../css/confocal.css', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        layout = QVBoxLayout()

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)

        # Add the plot generated after program execution to the layout
        self.plot1 = pg.PlotWidget()
        self.plot1.plot(np.random.normal(size=100))
        layout.addWidget(self.plot1)

        # Add the live data plot to the layout
        self.plot2 = pg.PlotWidget()
        # self.plot2.setYRange(0, 1)
        layout.addWidget(self.plot2)

        # Add the plot generated after program execution to the layout
        self.plot3 = pg.PlotWidget()
        self.plot3.plot(np.random.normal(size=100))
        layout.addWidget(self.plot3)

        # Set the layout for the main window
        self.setLayout(layout)

        # Create a timer to update the live data plot
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1)  # update the plot every 50 milliseconds

    def update_plot(self):
        # # Update the live data plot with new data
        # x = np.linspace(0, 10, 100)
        # y = np.random.rand(100)
        # self.plot2.plot(x, y)

        self.spad_time_total = 0
        self.x_data = []
        self.y_data = []

        while True:
            try:
                with nidaqmx.Task() as task:
                    task.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")
                    task.ci_channels[0].ci_count_edges_term = "/Dev1/PFI8"

                    ts = 0.001

                    task.start()
                    for total_block in range(int(1 / ts)):
                        cnt = task.read()
                        # time.sleep(0.0001)
                    #                 plt.show();
                self.x_data.append(self.spad_time_total)
                self.y_data.append(cnt)
                time_total = self.spad_time_total + ts
                print(self.y_data)
                self.plot2.plot(self.x_data, self.y_data)

            except nidaqmx.DaqError as e:
                print("An error occurred:", e)

            except Exception as e:
                print("An unexpected error occurred:", e)

            finally:
                task.close()