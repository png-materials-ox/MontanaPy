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

        # Parameters required to determine the mirror displacement voltage to image position
        self.mag = self.config["optics"]["mag"]                                     # Magnification of objective
        self.focal_length = self.config["optics"]["focal_length"]                   # mm
        self.f_tele = self.config["optics"]["f_tele"]                               # mm
        self.um_per_V_x = self.config["hardware"]["fsm"]["um_per_V_x"]              # um/V
        self.um_per_V_y = self.config["hardware"]["fsm"]["um_per_V_y"]              # um/V

        self.daq = DAQ()

    def get_position(self):
        channels = [self.x_channel, self.y_channel]
        voltages = self.daq.read_analogue_voltage(channels=channels)
        pos_x = self.voltage_to_position(voltages[0][0], self.um_per_V_x)
        pos_y = self.voltage_to_position(voltages[1][0], self.um_per_V_y)
        return (pos_x, pos_y)

    def voltage_to_position(self, vin, um_per_V):
        return vin * ((self.focal_length / self.mag) * (um_per_V / self.f_tele))