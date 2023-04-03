from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QApplication,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
import sys
import numpy as np

class Confocal(QWidget):
    def __init__(self):
        super().__init__()

        # Load stylesheet
        with open('../css/confocal.css', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.setWindowTitle("Confocal Window")
        layout = QVBoxLayout()

        # self.setLayout(layout)

        #TODO Work out how to put this in the css file.
        self.resize(1200, 800)

        # # Create the plot widget and add it to the layout
        self.plot_widget = pg.PlotWidget()

        # Set the layout for the main window
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt = Confocal()
    qt.show()
    sys.exit(app.exec())
