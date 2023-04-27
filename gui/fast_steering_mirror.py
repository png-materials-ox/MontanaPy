from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)
from PySide6.QtCore import Qt, QTimer, Slot
import pyqtgraph as pg
import numpy as np

import hardware.newport_fsm as nfsm
from gui.core import GUICore
from gui.threads.fsm_threads import ScanThread, PlotFSMThread


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

        core = FSMCore()
        self.fsm = core.fsm_components

        ########################################
        #### Create a grid layout container ####
        ########################################
        grid_layout = QGridLayout()
        grid_layout.addLayout(core.label_box, 0, 0)
        grid_layout.addLayout(core.button_box, 1, 0, 1, 2)
        grid_layout.addLayout(core.hbox, 2, 0, 1, 2)
        grid_layout.addWidget(core.plot_widget, 3, 0, 2, 2)
        self.setLayout(grid_layout) # Set the layout for the widget

        self.fsm_timer = core.timer
        self.fsm_timer.start(10)  # interval is in milliseconds

        self.show()


class FSMCore(GUICore):
    def __init__(self):
        super().__init__()

        # TODO: Need to work out how to properly get these from the input forms
        self.dwell_ms = 10
        self.xsteps = 100
        self.ysteps = 100
        self.roi = 60

        # Call a subclass which contains layout components for the FSM page
        self.fsm_components = FSMGuiComponents(self.xsteps, self.ysteps, self.roi, self.dwell_ms)
        self.fsm = nfsm.FSM()  # FSM hardware class

        # Calculate scan range
        sr = self.fsm.calc_scan_voltage_range(roi=self.roi)
        self.x = list(np.linspace(sr['x_min'], sr['x_max'], self.xsteps))
        self.y = list(np.linspace(sr['y_min'], sr['y_max'], self.xsteps))

        ########################
        #### Setup the plot ####
        ########################
        self.plot_widget = pg.PlotWidget()

        self.plot_widget.setXRange(min(self.x), max(self.x))
        self.plot_widget.setYRange(min(self.y), max(self.y))
        grad = super()._gradient_plot_backround(self.plot_widget)
        self.plot_widget.setBackgroundBrush(grad)  # set the background brush of the plot widget to the gradient

        # ####################################################
        # #### Buttons for starting and stopping FSM scan ####
        # ####################################################
        self.start_button = self.fsm_components.start_button
        self.stop_button = self.fsm_components.stop_button
        self.zero_button = self.fsm_components.zero_button
        self.button_box = self.fsm_components.button_box

        # Need to run the processes on different threads to prevent blocking
        self.scan_thread = ScanThread(self.fsm, self.x, self.y, self.dwell_ms)
        self.plot_thread = PlotFSMThread(self.plot_widget, self.x, self.y, self.dwell_ms)
        self.plot_thread.update_plot.connect(self.update_plot) # Connect method to signal from thread
        self.start_button.clicked.connect(self._on_start_click)
        self.stop_button.clicked.connect(self._on_stop_click)
        self.zero_button.clicked.connect(self.fsm.zero_fsm)

        #########################################################
        #### Forms for displaying the FSM x and y positions #####
        #########################################################
        self.label1 = self.fsm_components.label1
        self.label2 = self.fsm_components.label2
        self.hbox = self.fsm_components.hbox
        self.label_box = self.fsm_components.label_box

        # Connect a signal to input1 to store its text as a variable
        self.fsm_components.input_ms.returnPressed.connect(lambda: self._store_dwell_time(self.fsm_components.input_ms.text()))
        self.fsm_components.input_xsteps.returnPressed.connect(lambda: self._store_xsteps(self.fsm_components.input_xsteps.text()))
        self.fsm_components.input_ysteps.returnPressed.connect(lambda: self._store_ysteps(self.fsm_components.input_ysteps.text()))
        self.fsm_components.input_roi.returnPressed.connect(lambda: self._store_roi(self.fsm_components.input_roi.text()))

        # Create a timer to update the value every 10 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)


    def _store_dwell_time(self, text):
        self.dwell_ms = int(text) / 1000
        self.logging.info("Dwell time set to {:f} ms".format(self.dwell_time * 1000))

    def _store_xsteps(self, text):
        self.xsteps = int(text)
        self.logging.info("X steps time set to {:f}".format(self.xsteps))

    def _store_ysteps(self, text):
        self.ysteps = float(text)
        self.logging.info("Y steps time set to {:f}".format(self.ysteps))

    def _store_roi(self, text):
        self.roi = float(text)
        self.logging.info("ROI set to {:f}".format(self.roi))

    def _on_start_click(self):
        self.logging.info('FSM start button clicked')
        self.scan_thread.start()
        self.plot_thread.start()

    def _on_stop_click(self):
        self.logging.info('FSM stop button clicked')
        self.scan_thread.stop_flag = True
        self.plot_thread.stop_flag = True

    def update_position(self):
        self.pos_x, self.pos_y = self.fsm.get_position()
        self.label1.setText(str(self.pos_x))
        self.label2.setText(str(self.pos_y))

    @Slot(list, list)
    def update_plot(self, x, y):
        self.plot_widget.plot(x, y, pen=pg.mkPen(width=7, color='#ffa02f'), symbol='o', symbolPen='#ffa02f',
                              clear=True)

class FSMGuiComponents(GUICore):
    def __init__(self, xsteps, ysteps, roi, dwell_ms):
        super().__init__()

        self.dwell_ms = dwell_ms
        self.xsteps = xsteps
        self.ysteps = ysteps
        self.roi = roi

        ####################################################
        #### Buttons for starting and stopping FSM scan ####
        ####################################################

        self.button_grp1 = QGroupBox()
        self.button_grp2 = QGroupBox()
        self.button_grp3 = QGroupBox()

        self.start_button_box = QVBoxLayout()
        self.start_button = super()._create_button('Scan', self.start_button_box)

        self.stop_button_box = QVBoxLayout()
        self.stop_button = super()._create_button('Stop', self.stop_button_box)

        self.zero_button_box = QVBoxLayout()
        self.zero_button = super()._create_button('Zero FSM', self.zero_button_box)

        self.button_grp1.setLayout(self.start_button_box)
        self.button_grp2.setLayout(self.stop_button_box)
        self.button_grp3.setLayout(self.zero_button_box)

        self.button_box = QHBoxLayout()
        self.button_box.addWidget(self.button_grp1)
        self.button_box.addWidget(self.button_grp2)
        self.button_box.addWidget(self.button_grp3)

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
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.groupbox1)
        self.hbox.addWidget(self.groupbox2)

        # Create the three form inputs and their labels
        self.label_ms, self.input_ms = super()._create_label("Dwell time (ms)", "int", placeholder=str(self.dwell_ms))
        self.label_xsteps, self.input_xsteps = super()._create_label("X steps", "int", placeholder=str(self.xsteps))
        self.label_ysteps, self.input_ysteps = super()._create_label("Y steps", "int", placeholder=str(self.ysteps))
        self.label_roi, self.input_roi = super()._create_label("ROI", "int", placeholder=str(self.roi))

        self.label_box = QHBoxLayout()
        self.label_box.addWidget(self.label_ms)
        self.label_box.addWidget(self.input_ms)
        self.label_box.addWidget(self.label_xsteps)
        self.label_box.addWidget(self.input_xsteps)
        self.label_box.addWidget(self.label_ysteps)
        self.label_box.addWidget(self.input_ysteps)
        self.label_box.addWidget(self.label_roi)
        self.label_box.addWidget(self.input_roi)