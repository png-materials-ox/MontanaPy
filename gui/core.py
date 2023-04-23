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

    # def _open_window(self, obj, title):
    #     window = obj
    #     window.setWindowTitle(title)
    #     window.show()
    #     window.setParent(None)