from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QApplication,
    QVBoxLayout,
    QLabel,
)
import sys


class CutiePy(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO Create title bar

        # TODO Create logo
        # self.setWindowIcon(QTGui.QIcon("cutie-py.png"))

        # TODO Separate into tabs for instruments, programs, analysis, etc
        # self.resize(300, 420)
        self.setWindowTitle("Cutie Py")

        # Load stylesheet
        with open('css/main.css', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.layout = QVBoxLayout()

        # TODO This data should come from a config file, so it can be dynamic.
        self._options = ["AOM",
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

        self.buttons["Confocal"].clicked.connect(self.open_confocal_window)

    def _create_button(self, name):
        button = QPushButton(name)
        button.setObjectName(name)
        self.layout.addWidget(button)
        return button

    def open_confocal_window(self):
        self.confocal_window = Confocal()
        self.confocal_window.setWindowTitle("Confocal Window")
        self.confocal_window.show()


class Confocal(QWidget):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open('css/confocal.css', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        layout = QVBoxLayout()
        self.label = QLabel("Confocal")
        layout.addWidget(self.label)

        self.setLayout(layout)

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = CutiePy()
    qt.show()
    sys.exit(app.exec())
