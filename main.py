import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton
from gui.core import GUICore
from gui.aom import AOM
from gui.eom import EOM
from gui.wls import WLS
from gui.fast_steering_mirror import FSM
from gui.confocal import Confocal
from gui.single_photon_counter import SPC

import logging
import warnings
warnings.filterwarnings("ignore")

import ctypes
import sys

class MontanaPy(GUICore):
    """
    MontanaPy

    Control and analysis software for optical microscopy and control of quantum defect centers. MontanaPy is the main
    window presented to a user, providing navigation options.

    Version     : 0.1.0
    Author      : Gareth Siôn Jones
    Affiliation : Oxford University
    Department  : Department of Materials

    Attributes
    ----------

    Methods
    -------

    """
    def __init__(self, parent=None):
        super().__init__(parent)

        logging.basicConfig(filename='log/log.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')

        self.windows = []

        # Create the tabs
        self.tab_widget = QTabWidget()
        self.instruments_tab = QWidget()
        self.programs_tab = QWidget()
        self.analysis_tab = QWidget()

        # Add the tabs to the tab widget
        self.tab_widget.addTab(self.instruments_tab, "Instruments")
        self.tab_widget.addTab(self.programs_tab, "Programs")
        self.tab_widget.addTab(self.analysis_tab, "Analysis")

        # Set the layout for the instruments tab
        self.instruments_layout = QVBoxLayout()

        # TODO This data should come from a config file, so it can be dynamic.
        self._instrument_options = ["AOM",
                                    "EOM",
                                    "WLS",
                                    "Toptica Laser",
                                    "Single Photon Counter",
                                    "Fast Steering Mirror",
                                    "GEM 532",
                                    "Oscilloscope",
                                    "Wavemeter",
                                    "Power Meter",
                                    "Spectrometer",
                                    "Montana Piezos",
                                    "Montana Temperature",
                                    ]

        self._program_options = ["Confocal",
                         "PLE",
                         "Automate Grid Spectra Collection",
                         "Peak-Find"]

        self._analysis_options = ["PL Analysis",
                                 "Spectra Analysis"]

        self.instrument_buttons = {}
        for name in self._instrument_options:
            self.instrument_buttons["%s" % name] = super()._create_button(name, self.instruments_layout)

        self.instruments_layout.addStretch()
        self.instruments_tab.setLayout(self.instruments_layout)

        # Set the layout for the programs tab
        self.programs_layout = QVBoxLayout()

        self.program_buttons = {}
        for name in self._program_options:
            self.program_buttons["%s" % name] = super()._create_button(name, self.programs_layout)

        self.programs_layout.addStretch()
        self.programs_tab.setLayout(self.programs_layout)

        # Set the layout for the analysis tab
        self.analysis_layout = QVBoxLayout()

        self.analysis_buttons = {}
        for name in self._analysis_options:
            self.analysis_buttons["%s" % name] = super()._create_button(name, self.analysis_layout)

        self.analysis_layout.addStretch()
        self.analysis_tab.setLayout(self.analysis_layout)

        # Set the main layout for the widget
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

        # Set the window properties
        self.setWindowTitle("Montana Py")
        self.setGeometry(300, 300, 300, 300)

        # Load stylesheet
        with open("css/main.css", "r") as f:
            style = f.read()
            self.setStyleSheet(style)

        self.instrument_buttons["AOM"].clicked.connect(lambda: self._open_window(self, AOM(), "AOM Window"))
        self.instrument_buttons["EOM"].clicked.connect(lambda: self._open_window(self, EOM(), "EOM Window"))
        self.instrument_buttons["WLS"].clicked.connect(lambda: self._open_window(self, WLS(), "WLS Window"))
        self.instrument_buttons["Single Photon Counter"].clicked.connect(lambda: self._open_window(self, SPC(), "SPC Window"))
        self.instrument_buttons["Fast Steering Mirror"].clicked.connect(lambda: self._open_window(self, FSM(), "FSM Window"))
        self.program_buttons["Confocal"].clicked.connect(lambda: self._open_window(self, Confocal(), "Confocal Window"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = MontanaPy()
    qt.show()
    sys.exit(app.exec())
