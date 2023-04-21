import nidaqmx

class WLS_Ctrl:
    def __init__(self):
        self.channel = "Dev1/port0/line0"

    def write_high(self):
        with nidaqmx.Task() as task:
            # Set the digital output pin to high
            task.do_channels.add_do_chan(self.channel)
            task.write(True)

    def write_low(self):
        with nidaqmx.Task() as task:
            # Set the digital output pin to low
            task.do_channels.add_do_chan(self.channel)
            task.write(False)