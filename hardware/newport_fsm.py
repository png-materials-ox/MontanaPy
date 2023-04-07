import numpy as np
import os
import time
import json
# import nidaqmx


class FSM:

    def __init__(self):
        _cfg_file = open(os.path.join(os.getcwd() + "\\config\\config.json"))
        self.config = json.load(_cfg_file)
        self.x_channel = self.config['hardware']['nicard']['fsm_x_volt_chan']
        self.y_channel = self.config['hardware']['nicard']['fsm_y_volt_chan']

        # TODO get from config file
        # Parameters required to determine the mirror displacement voltage to image position
        self.mag = 100              # Magnification of objective
        self.focal_length = 160     # mm
        self.f_tele = 400           # mm
        self.um_per_V_x = 2258.976  # um/V
        self.um_per_V_y = 1557.688  # u,/V

    def read_analogue_in(self):
        ''' This will go into the DAQ class'''

        channels = [self.x_channel, self.y_channel]
        # Create a DAQ session
        with nidaqmx.Task() as task:
            # Configure the input channels
            for channel in channels:
                task.ai_channels.add_ai_voltage_chan(channel)

            task.ai_channels.all.ai_min = -10
            task.ai_channels.all.ai_max = 10

            # Set the acquisition parameters
            task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Start the acquisition
            task.start()

            # Read and print the data
            while True:
                data = task.read(number_of_samples_per_channel=1)
                x = data[0][0]
                y = data[1][0]
                x_disp = self.voltage_to_position(x, self.um_per_V_x)
                y_disp = self.voltage_to_position(y, self.um_per_V_y)
                print(f"Input x: {x}, Input y: {y}")
                print(f"Disp x: {x_disp}, Disp y: {y_disp}")

                # Wait for 10ms
                time.sleep(0.01)

    def voltage_to_position(self, vin, um_per_V):
        return vin * ((self.focal_length / self.mag) * (um_per_V / self.f_tele))


fsm = FSM()
fsm.read_analogue_in()