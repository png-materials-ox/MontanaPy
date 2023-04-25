from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QApplication
)
import sys
from PySide6.QtCore import Qt, QTimer, QThread, QObject, Signal, Slot
import pyqtgraph as pg

import hardware.newport_fsm as nfsm
from gui.core import GUICore

import numpy as np

import logging

logging.basicConfig(filename='log/log.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')

class FSM(GUICore):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open("css/fast_steering_mirror.css", "r") as f:
            style = f.read()
            self.setStyleSheet(style)

        # Set the window properties
        self.setWindowTitle("Display Values and Plot")
        self.setGeometry(200, 200, 800, 600)

        # self.x = [i * 0.001 for i in range(101)]
        # self.y = [i * 0.001 for i in range(101)]
        self.dwell_ms = 10
        self.xsteps = 100
        self.ysteps = 100
        self.roi = 60

        self.fsm = nfsm.FSM()
        sr = self.fsm.calc_scan_voltage_range(roi=self.roi)

        self.x = list(np.linspace(sr['x_min'], sr['x_max'], self.xsteps))
        self.y = list(np.linspace(sr['y_min'], sr['y_max'], self.xsteps))

        ########################
        #### Setup the plot ####
        ########################
        self.plot_widget = pg.PlotWidget()

        self.plot_widget.setXRange(min(self.x), max(self.x), padding=0)
        self.plot_widget.setYRange(min(self.y), max(self.y), padding=0)
        grad = GUICore._gradient_plot_backround(self.plot_widget)

        # set the background brush of the plot widget to the gradient
        self.plot_widget.setBackgroundBrush(grad)

        ####################################################
        #### Buttons for starting and stopping FSM scan ####
        ####################################################

        self.button_grp1 = QGroupBox()
        self.button_grp2 = QGroupBox()
        self.button_grp3 = QGroupBox()

        self.start_button_box = QVBoxLayout()
        start_button = super()._create_button('Scan', self.start_button_box)

        self.stop_button_box = QVBoxLayout()
        stop_button = super()._create_button('Stop', self.stop_button_box)

        self.zero_button_box = QVBoxLayout()
        zero_button = super()._create_button('Zero FSM', self.zero_button_box)

        self.button_grp1.setLayout(self.start_button_box)
        self.button_grp2.setLayout(self.stop_button_box)
        self.button_grp3.setLayout(self.zero_button_box)

        self.button_box = QHBoxLayout()
        self.button_box.addWidget(self.button_grp1)
        self.button_box.addWidget(self.button_grp2)
        self.button_box.addWidget(self.button_grp3)

        #################################
        #### Forms for Scan Settings ####
        #################################

        self.scan_thread = ScanThread(self.fsm, self.x, self.y, self.dwell_ms)
        self.plot_thread = PlotFSMThread(self.plot_widget, self.x, self.y, self.dwell_ms)
        self.plot_thread.update_plot.connect(self.update_plot)
        start_button.clicked.connect(self._on_start_click)
        stop_button.clicked.connect(self._on_stop_click)
        zero_button.clicked.connect(self.fsm.zero_fsm)

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

        # Create the three form inputs and their labels
        label_ms, input_ms = super()._create_label("Dwell time (ms)", "int", placeholder=str(self.dwell_ms))
        label_xsteps, input_xsteps = super()._create_label("X steps", "int", placeholder=str(self.xsteps))
        label_ysteps, input_ysteps = super()._create_label("Y steps", "int", placeholder=str(self.ysteps))
        label_roi, input_roi = super()._create_label("ROI", "int", placeholder=str(self.roi))

        label_box = QHBoxLayout()
        label_box.addWidget(label_ms)
        label_box.addWidget(input_ms)
        label_box.addWidget(label_xsteps)
        label_box.addWidget(input_xsteps)
        label_box.addWidget(label_ysteps)
        label_box.addWidget(input_ysteps)
        label_box.addWidget(label_roi)
        label_box.addWidget(input_roi)

        ########################################
        #### Create a grid layout container ####
        ########################################
        grid_layout = QGridLayout()
        grid_layout.addLayout(label_box, 0, 0)
        grid_layout.addLayout(self.button_box, 1, 0, 1, 2)
        grid_layout.addLayout(hbox, 2, 0, 1, 2)
        grid_layout.addWidget(self.plot_widget, 3, 0, 2, 2)

        # Set the layout for the widget
        self.setLayout(grid_layout)

        # Create a timer to update the value every 10 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # interval is in milliseconds
        # super().qtimer(self.update_position, 10)

        self.show()

        # Connect a signal to input1 to store its text as a variable
        input_ms.returnPressed.connect(lambda: self._store_dwell_time(input_ms.text()))
        input_xsteps.returnPressed.connect(lambda: self._store_xsteps(input_xsteps.text()))
        input_ysteps.returnPressed.connect(lambda: self._store_ysteps(input_ysteps.text()))
        input_roi.returnPressed.connect(lambda: self._store_roi(input_roi.text()))

    def _store_dwell_time(self, text):
        self.dwell_time = int(text) / 1000
        logging.info("Dwell time set to {:f} ms".format(self.dwell_time*1000))

    def _store_xsteps(self, text):
        self.xsteps = int(text)
        logging.info("X steps time set to {:f}".format(self.xsteps))

    def _store_ysteps(self, text):
        self.ysteps = float(text)
        logging.info("Y steps time set to {:f}".format(self.ysteps))

    def _store_roi(self, text):
        self.roi = float(text)
        logging.info("ROI set to {:f}".format(self.roi))

    def update_position(self):
        self.pos_x, self.pos_y = self.fsm.get_position()
        self.label1.setText(str(self.pos_x))
        self.label2.setText(str(self.pos_y))

    @Slot(list, list)
    def update_plot(self, x, y):
        self.plot_widget.plot(x, y, pen=pg.mkPen(width=7, color='#ffa02f'), symbol='o', symbolPen='#ffa02f', clear=True)

    def _on_start_click(self):
        logging.info('FSM start button clicked')
        self.scan_thread.start()
        self.plot_thread.start()

    def _on_stop_click(self):
        logging.info('FSM stop button clicked')
        self.scan_thread.stop_flag = True
        # self.scan_thread.terminate()
        self.plot_thread.stop_flag = True


class ScanThread(QThread):
    def __init__(self, fsm, x, y, dwell_ms):
        super().__init__()

        logging.info('ScanThread called')

        self.stop_flag = False
        self.fsm = fsm
        self.x = x
        self.y = y
        self.dwell_ms = dwell_ms

        self.stop_flag = False

        # self.plot_updated = Signal(float, float)

    def run(self):
        logging.info('ScanThread run')
        # while not self.stop_flag:
        #     self.fsm.scan_xy(x=self.x, y=self.y, dwell_ms=self.dwell_ms)
        # logging.info('ScanThread stopped')
        # return
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                if self.stop_flag:
                    logging.info('ScanThread stopped')
                    return
                self.fsm.scan_xy(x=self.x[i], y=self.y[j], dwell_ms=self.dwell_ms)


class PlotFSMThread(QThread):
    update_plot = Signal(list, list)

    def __init__(self, plot_widget, x, y, dwell_ms):
        super().__init__()
        self.plot_widget = plot_widget
        self.x = x
        self.y = y
        self.dwell_ms = dwell_ms
        self.stop_flag = False

        logging.info('PlotThread called')

    def run(self):
        logging.info('PlotThread run')
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                if self.stop_flag:
                    logging.info('PlotThread stopped')
                    return
                self.update_plot.emit([self.y[j]], [self.x[i]])
                self.msleep(self.dwell_ms)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     qt = FSM()
#     qt.show()
#     sys.exit(app.exec())