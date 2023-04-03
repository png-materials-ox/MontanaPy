from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QApplication,
    QVBoxLayout,
    QLabel,
)
import sys

from aom import AOM
from eom import EOM
from confocal import Confocal

import warnings
warnings.filterwarnings("ignore")


class MontanaPy(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO Create title bar

        # TODO Create logo
        # self.setWindowIcon(QTGui.QIcon("cutie-py.png"))

        # TODO Separate into tabs for instruments, programs, analysis, etc
        # self.resize(300, 420)
        self.setWindowTitle("Montana Py")

        # Load stylesheet
        with open('css/main.css', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.layout = QVBoxLayout()

        # TODO This data should come from a config file, so it can be dynamic.
        self._options = ["AOM",
                         "EOM",
                         "WLS",
                         "Toptica Laser",
                         "GEM 532",
                         "Oscilloscope",
                         "Wavemeter",
                         "Spectrometer",
                         "Montana Piezos",
                         "Confocal",
                         "PLE",
                         "Automate Grid Spectra Collection",
                         "Peak-Find"]
        self.buttons = {}
        for name in self._options:
            self.buttons["%s" % name] = self._create_button(name)

        self.setLayout(self.layout)

        self.buttons["AOM"].clicked.connect(self.open_aom_window)
        self.buttons["EOM"].clicked.connect(self.open_eom_window)
        self.buttons["Confocal"].clicked.connect(self.open_confocal_window)

    def _create_button(self, name):
        button = QPushButton(name)
        button.setObjectName(name)
        self.layout.addWidget(button)
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
