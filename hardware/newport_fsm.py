import numpy as np
import os
import time
import json
from hardware.nidaq import DAQ


class FSM:

    def __init__(self):
        _cfg_file = open(os.path.join(os.getcwd() + "\\config\\config.json"))
        self.config = json.load(_cfg_file)

        self.x_channel = self.config['hardware']['nicard']['fsm_x_volt_chan']
        self.y_channel = self.config['hardware']['nicard']['fsm_y_volt_chan']

        self.x_channel = self.config['hardware']['nicard']['fsm_x_volt_chan']
        self.y_channel = self.config['hardware']['nicard']['fsm_y_volt_chan']

        self.fsm_x_chan_o = self.config['hardware']['nicard']["scan_x"]
        self.fsm_y_chan_o = self.config['hardware']['nicard']["scan_y"]

        # Parameters required to determine the mirror displacement voltage to image position
        self.mag = self.config["optics"]["mag"]                                     # Magnification of objective
        self.focal_length = self.config["optics"]["focal_length"]                   # mm
        self.f_tele = self.config["optics"]["f_tele"]                               # mm
        self.um_per_V_x = self.config["hardware"]["fsm"]["um_per_V_x"]              # um/V
        self.um_per_V_y = self.config["hardware"]["fsm"]["um_per_V_y"]              # um/V

        self.daq = DAQ()

    def get_voltages(self):
        channels = [self.x_channel, self.y_channel]
        return self.daq.read_analogue_voltage(channels=channels)

    def get_position(self):
        voltages = self.get_voltages()
        pos_x = self.voltage_to_position(voltages[0][0], self.um_per_V_x)
        pos_y = self.voltage_to_position(voltages[1][0], self.um_per_V_y)
        return (pos_x, pos_y)

    def zero_fsm(self):
        self.daq.set_ao_voltage(self.fsm_x_chan_o, 0)
        self.daq.set_ao_voltage(self.fsm_y_chan_o, 0)


    def voltage_to_position(self, vin, um_per_V):
        return vin * ((self.focal_length / self.mag) * (um_per_V / self.f_tele))

    def position_to_voltage(self, position, um_per_V):
        return position / ((self.focal_length / self.mag) * (um_per_V / self.f_tele))

    def scan_xy(self, x=[], y=[], dwell_ms=10):
        # self.daq.scan_xy(x_waveform=x, y_waveform=y, dwell_ms=dwell_ms)
        self.daq.scan_xy(x=x, y=y, dwell_ms=dwell_ms)
    def calc_scan_voltage_range(self, roi=50):
        # If the ROI is not selected, zero the FSM
        self.zero_fsm()

        x_min = self.position_to_voltage(-.5*roi*1e-03, self.um_per_V_x)
        x_max = self.position_to_voltage(.5 * roi * 1e-03, self.um_per_V_x)
        y_min = self.position_to_voltage(-.5 * roi * 1e-03, self.um_per_V_y)
        y_max = self.position_to_voltage(.5 * roi * 1e-03, self.um_per_V_y)

        return {"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max}