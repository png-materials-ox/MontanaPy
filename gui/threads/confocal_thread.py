from PySide6.QtCore import Qt, QTimer, QThread, QObject, Signal, Slot
import logging

logging.basicConfig(filename='log/log.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(message)s')


class ScanThread(QThread):
    '''
    Opens a new thread for scanning the FSM
    '''
    def __init__(self, fsm, x, y, dwell_ms):
        super().__init__()

        logging.info('ScanThread called')

        self.stop_flag = False
        self.fsm = fsm
        self.x = x
        self.y = y
        self.dwell_ms = dwell_ms

        self.stop_flag = False

    def run(self):
        logging.info('ScanThread run')
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                if self.stop_flag:
                    logging.info('ScanThread stopped')
                    return
                self.fsm.scan_xy(x=self.x[i], y=self.y[j], dwell_ms=self.dwell_ms)


class PlotFSMThread(QThread):
    '''
        Opens a new thread for plotting the FSM position
        '''

    # Signal for the update_plot function, to be passed and called in the main script
    update_plot = Signal(list, list)

    def __init__(self, plot_widget, x, y, dwell_ms):
        '''
        Constructor for the PlotFSMThread class

        :param plot_widget: A PyQtGraph.plotWidget() object
        :param x: List of x voltage values for the FSM
        :param y: List of y voltage values for the FSM
        :param dwell_ms: Dwell time of the FSM
        '''
        super().__init__()
        self.plot_widget = plot_widget
        self.x = x
        self.y = y
        self.dwell_ms = dwell_ms
        self.stop_flag = False

        logging.info('PlotThread called')

    def run(self):
        '''
        Runs the PlotFSM thread upon execution
        :return:
        '''
        logging.info('PlotThread run')
        for i in range(len(self.x)):
            for j in range(len(self.y)):
                if self.stop_flag:
                    logging.info('PlotThread stopped')
                    return
                else:
                    # Update the x and y positions on the plot. Attaches the signals to the update_plot variable
                    self.update_plot.emit([self.y[j]], [self.x[i]])
                    self.msleep(self.dwell_ms)

class PlotScanThread(QThread):
    '''
    Opens a thread for plotting the scan image.
    '''
    def __init__(self):
        super().__init__()

    def run(self):
        pass

class SPCThread(QThread):
    '''
    Opends a thread for running the SPAD.
    '''
    def __init__(self):
        super().__init__()

    def run(self):
        pass