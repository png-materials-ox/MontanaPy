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
from PySide6.QtCore import Qt, QTimer, QThread, QObject, Signal, Slot
import pyqtgraph as pg

import hardware.newport_fsm as nfsm
from gui.core import GUICore

import time

import logging

logging.basicConfig(filename='log/log.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')

import numpy as np

class ScanThread(QThread):
    def __init__(self, fsm, x, y, dwell_ms):
        super().__init__()

        logging.info('ScanThread called')

        self.stop_flag = False
        self.fsm = fsm
        self.x = x
        self.y = y
        self.dwell_ms = dwell_ms

        # self.plot_updated = Signal(float, float)

    def run(self):
        logging.info('ScanThread run')
        self.fsm.scan_xy(x=self.x, y=self.y, dwell_ms=self.dwell_ms)


class PlotFSMThread(QThread):
    update_plot = Signal(list, list)

    def __init__(self, plot_widget, x, y, dwell_ms):
        super().__init__()
        self.plot_widget = plot_widget
        self.x = x
        self.y = y
        self.dwell_ms = dwell_ms

        logging.info('PlotThread called')

    def run(self):
        logging.info('PlotThread run')
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                self.update_plot.emit([self.y[j]], [self.x[i]])
                self.msleep(self.dwell_ms)

    # def update_fsm_plot(self):
    #     for i in range(len(self.x)):
    #         for j in range(len(self.y)):
    #             self.plot_widget.plot([self.y[j]], [self.x[i]], pen=None, symbol='o', symbolPen='r', clear=True)
    #             time.sleep(self.dwell_ms)
    # def stop(self):
    #     self.stop_event.set()


class FSM(GUICore):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open("css/fast_steering_mirror.css", "r") as f:
            style = f.read()
            self.setStyleSheet(style)

        self.plot_widget = pg.PlotWidget()

        # Set the window properties
        self.setWindowTitle("Display Values and Plot")
        self.setGeometry(100, 100, 400, 300)

        ####################################################
        #### Buttons for starting and stopping FSM scan ####
        ####################################################
        self.fsm = nfsm.FSM()

        self.button_grp1 = QGroupBox()
        self.button_grp2 = QGroupBox()

        self.start_button_box = QVBoxLayout()
        start_button = super()._create_button('Scan', self.start_button_box)

        self.stop_button_box = QVBoxLayout()
        stop_button = super()._create_button('Stop', self.stop_button_box)

        self.button_grp1.setLayout(self.start_button_box)
        self.button_grp2.setLayout(self.stop_button_box)

        self.button_box = QHBoxLayout()
        self.button_box.addWidget(self.button_grp1)
        self.button_box.addWidget(self.button_grp2)

        #################################
        #### Forms for Scan Settings ####
        #################################

        # x = list(np.linspace(0.001, 0.1, 101))
        # y = list(np.linspace(0.001, 0.1, 101))
        x = [i * 0.001 for i in range(101)]
        y = [i * 0.001 for i in range(101)]
        self.scan_thread = ScanThread(self.fsm, x, y, 100)
        self.plot_thread = PlotFSMThread(self.plot_widget, x, y, 100)
        self.plot_thread.update_plot.connect(self.update_plot)
        start_button.clicked.connect(self._on_start_click)

        #########################################################
        #### Forms for displaying the FSM x and y positions #####
        #########################################################
        self.groupbox1 = QGroupBox("FSM x")
        self.groupbox2 = QGroupBox("FSM y")

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

        ########################
        #### Setup the plot ####
        ########################

        self.plot_widget.setXRange(min(x), max(x), padding=0)
        self.plot_widget.setXRange(min(y),max(y), padding=0)
        grad = GUICore._gradient_plot_backround(self.plot_widget)

        # set the background brush of the plot widget to the gradient
        self.plot_widget.setBackgroundBrush(grad)

        ########################################
        #### Create a grid layout container ####
        ########################################
        grid_layout = QGridLayout()
        grid_layout.addLayout(self.button_box, 0, 0)
        grid_layout.addLayout(hbox, 1, 0)
        grid_layout.addWidget(self.plot_widget, 2, 0)

        # Set the layout for the widget
        self.setLayout(grid_layout)

        # Create a timer to update the value every 10 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # interval is in milliseconds
        # super().qtimer(self.update_position, 10)

        self.show()

    def update_position(self):
        self.pos_x, self.pos_y = self.fsm.get_position()
        self.label1.setText(str(self.pos_x))
        self.label2.setText(str(self.pos_y))

    @Slot(list, list)
    def update_plot(self, x, y):
        logging.info('Plotting FSM')
        self.plot_widget.plot(x, y, pen=None, symbol='o', symbolPen='r', clear=True)

    def _on_start_click(self):
        logging.info('FSM start button clicked')
        self.scan_thread.start()
        self.plot_thread.start()

    # def _on_stop_click(self):
    #     logging.info('FSM stop button clicked')
    #     self.scan_thread.stop()
    #     self.plot_thread.stop()