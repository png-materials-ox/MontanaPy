import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox
)
from PySide6.QtCore import Qt


class FSM(QWidget):
    def __init__(self, value1, value2):
        super().__init__()

        # Create group boxes to hold the values
        self.groupbox1 = QGroupBox("Value 1")
        self.groupbox2 = QGroupBox("Value 2")

        # Create labels to display the values
        self.label1 = QLabel(str(value1))
        self.label2 = QLabel(str(value2))

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

        # Create a horizontal layout for the two group boxes
        hbox = QHBoxLayout()

        # Add the group boxes to the layout
        hbox.addWidget(self.groupbox1)
        hbox.addWidget(self.groupbox2)

        # Set the layout for the widget
        self.setLayout(hbox)

        # Set the window properties
        self.setWindowTitle("Display Values")
        self.setGeometry(100, 100, 400, 100)
        self.show()


if __name__ == '__main__':
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create a widget and display the values within it
    value1 = 42
    value2 = 100
    display_values = FSM(value1, value2)

    # Run the application
    sys.exit(app.exec_())
