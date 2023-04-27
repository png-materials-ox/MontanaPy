from PySide6.QtCore import QThread
from gui.core import GUICore


class SPCThread(QThread):
    '''
    Opens a new thread for acquiring the SPC
    '''
    def __init__(self, spc):
        super().__init__()

        self.logging = GUICore().logging
        self.logging.info('SPCThread called')

        self.spc = spc

    def run(self):
        self.logging.info('SPCThread run')