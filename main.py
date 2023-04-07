import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton
from gui.aom import AOM
from gui.eom import EOM
from gui.confocal import Confocal
from gui.single_photon_counter import SPC

import warnings
warnings.filterwarnings("ignore")


class MontanaPy(QWidget):
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

    _create_instr_button(name)
        Creates buttons in the main GUI for the instument panel

    _create_prog_button(name)
        Creates buttons in the main GUI for the program panel

    _create_analysis_button(name)
        Creates buttons in the main GUI for the analysis panel

    _open_aom_window()
        Opens the AOM instrument control window

    _open_eom_window()
        Opens the EOM instrument control window

    _open_confocal_window()
        Opens the Confocal program windwow
    """
    def __init__(self, parent=None):
        super().__init__(parent)

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
            self.instrument_buttons["%s" % name] = self._create_instr_button(name)

        self.instruments_layout.addStretch()
        self.instruments_tab.setLayout(self.instruments_layout)

        # Set the layout for the programs tab
        self.programs_layout = QVBoxLayout()

        self.program_buttons = {}
        for name in self._program_options:
            self.program_buttons["%s" % name] = self._create_prog_button(name)

        self.programs_layout.addStretch()
        self.programs_tab.setLayout(self.programs_layout)

        # Set the layout for the analysis tab
        self.analysis_layout = QVBoxLayout()

        self.analysis_buttons = {}
        for name in self._analysis_options:
            self.analysis_buttons["%s" % name] = self._create_analysis_button(name)

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

        self.instrument_buttons["AOM"].clicked.connect(self._open_aom_window)
        self.instrument_buttons["EOM"].clicked.connect(self._open_eom_window)
        self.instrument_buttons["Single Photon Counter"].clicked.connect(self._open_spc_window)
        self.program_buttons["Confocal"].clicked.connect(self._open_confocal_window)

    def _create_instr_button(self, name):
        button = QPushButton(name)
        button.setObjectName(name)
        self.instruments_layout.addWidget(button)
        return button

    def _create_prog_button(self, name):
        button = QPushButton(name)
        button.setObjectName(name)
        self.programs_layout.addWidget(button)
        return button

    def _create_analysis_button(self, name):
        button = QPushButton(name)
        button.setObjectName(name)
        self.analysis_layout.addWidget(button)
        return button

    def _open_aom_window(self):
        self.aom_window = AOM()
        self.aom_window.setWindowTitle("AOM Window")
        self.aom_window.show()
        self.aom_window.setParent(None)

    def _open_spc_window(self):
        self.spc_window = SPC()
        self.spc_window.setWindowTitle("SPC Window")
        self.spc_window.show()
        self.spc_window.setParent(None)

    def _open_eom_window(self):
        self.eom_window = EOM()
        self.eom_window.setWindowTitle("EOM Window")
        self.eom_window.show()
        self.eom_window.setParent(None)

    def _open_confocal_window(self):
        self.confocal_window = Confocal()
        self.confocal_window.setWindowTitle("Confocal Window")
        self.confocal_window.show()
        self.confocal_window.setParent(None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = MontanaPy()
    qt.show()
    sys.exit(app.exec())
