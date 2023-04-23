from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPushButton
)

class GUICore(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _create_button(self, name, layout):
        button = QPushButton(name)
        button.setObjectName(name)
        layout.addWidget(button)
        return button