from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
    QPushButton,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLabel,
)
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
import os

from gui.core import GUICore

class Confocal(GUICore):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\confocal.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)

        self.fsm_components = FSMGuiComponents()

        ########################################
        #### Create a grid layout container ####
        ########################################
        grid_layout = QGridLayout()
        # grid_layout.addLayout(label_box, 0, 0)
        # grid_layout.addLayout(self.button_box, 1, 0, 1, 2)
        # grid_layout.addLayout(hbox, 2, 0, 1, 2)
        # grid_layout.addWidget(self.plot_widget, 3, 0, 2, 2)

class FSMGuiComponents(GUICore):
    def __init__(self):
        super().__init__()

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
        hbox = QHBoxLayout()
        hbox.addWidget(self.groupbox1)
        hbox.addWidget(self.groupbox2)

        # Create the three form inputs and their labels
        label_ms, input_ms = super()._create_label("Dwell time (ms)", "int", placeholder=str(self.dwell_ms))
        label_xsteps, input_xsteps = super()._create_label("X steps", "int", placeholder=str(self.xsteps))
        label_ysteps, input_ysteps = super()._create_label("Y steps", "int", placeholder=str(self.ysteps))
        label_roi, input_roi = super()._create_label("ROI", "int", placeholder=str(self.roi))

        self.label_box = QHBoxLayout()
        self.label_box.addWidget(label_ms)
        self.label_box.addWidget(input_ms)
        self.label_box.addWidget(label_xsteps)
        self.label_box.addWidget(input_xsteps)
        self.label_box.addWidget(label_ysteps)
        self.label_box.addWidget(input_ysteps)
        self.label_box.addWidget(label_roi)
        self.label_box.addWidget(input_roi)