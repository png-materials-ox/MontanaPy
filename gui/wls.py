import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

from instr_ctrl.wls_ctrl import WLS_Ctrl


class WLS(QWidget):
    def __init__(self):
        super().__init__()

        self.wls_ctrl = WLS_Ctrl()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.resize(200, 400)

        # layout.addStretch()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.setContentsMargins(0, 120, 0, 0)
        layout.setSpacing(0)
        # layout.setFixedSize(200, 400)

        self.button = QPushButton()
        self.button.setText("WLS\nOff")
        self.button.setCheckable(True)
        self.button.setChecked(False)

        # Load stylesheet
        with open(os.path.join(os.getcwd() + "\\css\\wls.css"), 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.button.clicked.connect(self.on_clicked)
        self.button.setFixedWidth(100)
        self.button.setFixedHeight(100)
        layout.addWidget(self.button)

        layout.addStretch()

    def on_clicked(self):
        if self.button.isChecked():
            self.button.setText("WLS\nOn")
            self.wls_ctrl.write_high()
        else:
            self.button.setText("WLS\nOff")
            self.wls_ctrl.write_low()