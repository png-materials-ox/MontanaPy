import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QThread, Signal, QObject

class PlotThread(QObject):
    plot_generated = Signal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        # Generate some data and plot it
        x = np.linspace(0, 10, 1000)
        y = np.sin(x)

        # Emit a signal with the plot data
        self.plot_generated.emit((x, y))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plot Window")

        # Create the plot widget and add it to the layout
        self.plot_widget = pg.PlotWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_layout.addWidget(self.plot_widget)

        self.plot_thread = QThread()
        self.plot_worker = PlotThread()

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(self.plot_layout)
        self.setCentralWidget(central_widget)

    def update_plot(self, plot_data):
        # Update the plot with the new data
        x, y = plot_data
        self.plot_widget.plot(x, y)

class ButtonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Window")

        # Create a button to generate the plot
        self.button = QPushButton("Generate Plot")
        self.button.clicked.connect(self.generate_plot)
        self.setCentralWidget(self.button)

        # Create the main window object but do not show it yet
        self.main_window = MainWindow()

    def generate_plot(self):
        # Create the plot thread and connect its signal to the main window's update_plot method

        self.plot_worker.moveToThread(self.plot_thread)
        self.plot_thread.started.connect(self.plot_worker.run)
        self.plot_worker.plot_generated.connect(self.main_window.update_plot)
        self.plot_thread.start()

        # Show the main window
        self.main_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ButtonWindow()
    window.show()
    sys.exit(app.exec())
