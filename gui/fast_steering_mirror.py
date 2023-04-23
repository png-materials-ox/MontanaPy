import sys
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QLinearGradient
import hardware.newport_fsm as nfsm
import pyqtgraph as pg
import time
import numpy as np


class FSM(QWidget):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open("css/fast_steering_mirror.css", "r") as f:
            style = f.read()
            self.setStyleSheet(style)

        # Buttons for starting and stopping FSM scan
        self.fsm = nfsm.FSM()

        self.grpbutt1 = QGroupBox()
        self.grpbutt2 = QGroupBox()

        self.start_button_box = QVBoxLayout()
        start_button = QPushButton('Scan')
        start_button.setObjectName('Scan')
        self.start_button_box.addWidget(start_button)

        self.stop_button_box = QVBoxLayout()
        stop_button = QPushButton('Stop')
        stop_button.setObjectName('Stop')
        self.stop_button_box.addWidget(stop_button)

        self.grpbutt1.setLayout(self.start_button_box)
        self.grpbutt2.setLayout(self.stop_button_box)

        self.button_box = QHBoxLayout()
        self.button_box.addWidget(self.grpbutt1)
        self.button_box.addWidget(self.grpbutt2)

        x = list(np.linspace(0.001, 0.002, 11))
        y = list(np.linspace(0.001, 0.002, 11))
        start_button.clicked.connect(self.fsm.scan_xy(x=x, y=y, x_rate=10, y_rate=10))

        #
        # Create group boxes to hold the values and the plot
        self.groupbox1 = QGroupBox("Value 1")
        self.groupbox2 = QGroupBox("Value 2")

        self.pos_x = 0
        self.pos_y = 0

        # Create labels to display the values
        self.label1 = QLabel(str(self.pos_x))
        self.label2 = QLabel(str(self.pos_y))

        # Set the labels to be centered
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)

        # Create vertical layouts for the group boxes
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()

        # Add the labels to the layouts
        layout1.addWidget(self.label1)
        layout2.addWidget(self.label2)

        # Set the layouts for the group boxes
        self.groupbox1.setLayout(layout1)
        self.groupbox2.setLayout(layout2)

        # Create a horizontal layout for the group boxes
        hbox = QHBoxLayout()
        hbox.addWidget(self.groupbox1)
        hbox.addWidget(self.groupbox2)

        # Add the plot to the layout
        self.plot_widget = pg.PlotWidget()

        grad = QLinearGradient(0, 0, 0, self.plot_widget.height())
        grad.setColorAt(0, pg.mkColor('#565656'))
        grad.setColorAt(0.1, pg.mkColor('#525252'))
        grad.setColorAt(0.5, pg.mkColor('#4e4e4e'))
        grad.setColorAt(0.9, pg.mkColor('#4a4a4a'))
        grad.setColorAt(1, pg.mkColor('#464646'))

        # set the background brush of the plot widget to the gradient
        self.plot_widget.setBackgroundBrush(grad)

        # Create a grid layout to contain the horizontal layout and the plot
        grid_layout = QGridLayout()
        grid_layout.addLayout(self.button_box, 0, 0)
        # grid_layout.addLayout(self.stop_button_box, 0, 1)
        grid_layout.addLayout(hbox, 1, 0)
        grid_layout.addWidget(self.plot_widget, 2, 0)

        # Set the layout for the widget
        self.setLayout(grid_layout)

        # Set the window properties
        self.setWindowTitle("Display Values and Plot")
        self.setGeometry(100, 100, 400, 300)

        # Create plot
        # self.plot_widget.setLabel('bottom', 'X Axis Label')
        # self.plot_widget.setLabel('left', 'Y Axis Label')
        # self.plot_widget.setXRange(x_waveform[0], x_waveform[-1])
        # self.plot_widget.setYRange(y_waveform[0], y_waveform[-1])
        # last_point = self.plot_widget.plot([x_waveform[0]], [y_waveform[0]], pen=None, symbol='o', symbolPen='r')

        # # Update plot
        # for i in range(len(x_waveform)):
        #     for j in range(len(y_waveform)):
        #         last_point.setData(x=[x_waveform[j]], y=[y_waveform[i]])
        #         pg.QtGui.QGuiApplication.processEvents()
        #         time.sleep(0.1)


        # Create a timer to update the value every 10 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # interval is in milliseconds

        self.show()

    def update_position(self):
        self.pos_x, self.pos_y = self.fsm.get_position()
        self.label1.setText(str(self.pos_x))
        self.label2.setText(str(self.pos_y))

        # Update the plot
        self.plot_widget.plot([self.pos_x], [self.pos_y], pen=None, symbol='o', symbolPen='r', clear=True)

