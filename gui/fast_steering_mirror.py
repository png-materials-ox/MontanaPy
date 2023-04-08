import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox
)
from PySide6.QtCore import Qt, QTimer

import hardware.newport_fsm as nfsm


class FSM(QWidget):
    def __init__(self):
        super().__init__()

        self.fsm = nfsm.FSM()

        # Create group boxes to hold the values
        self.groupbox1 = QGroupBox("Value 1")
        self.groupbox2 = QGroupBox("Value 2")

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

        # Create a timer to update the value every 10 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # interval is in milliseconds

        self.show()

    def update_position(self):
        self.pos_x, self.pos_y = self.fsm.get_position()
        self.label1.setText(str(self.pos_x))
        self.label2.setText(str(self.pos_y))

#
# if __name__ == '__main__':
#     # Create the Qt application
#     app = QApplication(sys.argv)
#
#     # Create a widget and display the values within it
#     value1 = 42
#     value2 = 100
#     display_values = FSM(value1, value2)
#
#     # Run the application
#     sys.exit(app.exec_())


# class DisplayValue(QWidget):
#     def __init__(self, value):
#         super().__init__()
#
#         # Create a label to display the value
#         self.label = QLabel(str(value))
#         self.label.setAlignment(Qt.AlignCenter)
#
#         # Create a vertical layout and add the label to it
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#
#         # Set the layout for the widget
#         self.setLayout(layout)
#
#         # Set the window properties
#         self.setWindowTitle("Display Value")
#         self.setGeometry(100, 100, 200, 100)
#
#         # Create a timer to update the value every second
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_value)
#         self.timer.start(1000)  # interval is in milliseconds
#
#         self.show()
#
#     def update_value(self):
#         # Update the value displayed in the label
#         # For example, increment the value by 1
#         current_value = int(self.label.text())
#         new_value = current_value + 1
#         self.label.setText(str(new_value))
#
#
# if __name__ == '__main__':
#     # Create the Qt application
#     app = QApplication(sys.argv)
#
#     # Create a widget and display the value within it
#     value = 42
#     display_value = DisplayValue(value)
#
#     # Run the application
#     sys.exit(app.exec_())
