import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtGui, QtWidgets

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the input form widgets
        self.label = QtWidgets.QLabel('Enter the number of points:')
        self.text_edit = QtWidgets.QLineEdit()
        self.text_edit.setFixedSize(100, 30)
        self.button = QtWidgets.QPushButton('Generate plot')
        self.button.setFixedSize(100, 30)
        self.button.clicked.connect(self.on_button_click)

        # Create the plot widget
        self.plot_widget = pg.PlotWidget()

        # Set up the layout
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.text_edit, 0, 1)
        layout.addWidget(self.button, 0, 2)
        layout.addWidget(self.plot_widget, 1, 0, 1, 3)

        # Set the column stretch factors
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 0)

    def on_button_click(self):
        # Generate some random data
        n_points = int(self.text_edit.text())
        x = np.linspace(0, 10, n_points)
        y = np.random.normal(size=n_points)

        # Clear the plot widget and plot the data
        self.plot_widget.clear()
        self.plot_widget.plot(x, y, pen=None, symbol='o', symbolSize=5)


if __name__ == '__main__':
    # Create the application
    app = QtWidgets.QApplication([])

    # Create and show the window
    window = MyWindow()
    window.show()

    # Run the event loop
    app.exec_()
