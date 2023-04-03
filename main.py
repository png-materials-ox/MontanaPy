import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton
from gui.aom import AOM
from gui.eom import EOM
from gui.confocal import Confocal

import warnings
warnings.filterwarnings("ignore")


class MontanaPy(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
                                    "GEM 532",
                                    "Oscilloscope",
                                    "Wavemeter",
                                    "Spectrometer",
                                    "Montana Piezos",
                                    "Power Meter"
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

        self.instrument_buttons["AOM"].clicked.connect(self.open_aom_window)
        self.instrument_buttons["EOM"].clicked.connect(self.open_eom_window)
        self.program_buttons["Confocal"].clicked.connect(self.open_confocal_window)

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

    def open_aom_window(self):
        self.aom_window = AOM()
        self.aom_window.setWindowTitle("AOM Window")
        self.aom_window.show()

    def open_eom_window(self):
        self.aom_window = EOM()
        self.aom_window.setWindowTitle("EOM Window")
        self.aom_window.show()

    def open_confocal_window(self):
        self.confocal_window = Confocal()
        self.confocal_window.setWindowTitle("Confocal Window")
        self.confocal_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = MontanaPy()
    qt.show()
    sys.exit(app.exec())
