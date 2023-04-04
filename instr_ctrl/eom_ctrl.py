import nidaqmx

class EOM_Ctrl:
    def __init__(self):
        self.channel = "Dev1/port0/line5"

    def write_high(self):
        with nidaqmx.Task() as task:
            # Set the digital output pin to high
            task.do_channels.add_do_chan(self.channel)
            task.write(True)

    def write_low(self):
        with nidaqmx.Task() as task:
            # Set the digital output pin to high
            task.do_channels.add_do_chan(self.channel)
            task.write(False)