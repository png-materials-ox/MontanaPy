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