import nidaqmx
import time
import json
import os


class DAQ:
    def __init__(self):

        _cfg_file = open(os.path.join(os.getcwd() + "\\config\\config.json"))
        self.config = json.load(_cfg_file)
        self.daq = self.config["hardware"]["nicard"]        # Daq device ID
        self.ctr_chan = self.daq["counter_channels"][0]     # DAQ channel for single photon counting
        self.photon_term = self.daq["photon_sources"][0]    # Associated timing channel for single photon counting

        # self.fsm_x_chan = self.daq + "/ai0"              # Fast steering mirror x
        # self.fsm_y_chan = self.daq + "/ai1"              # Fast steering mirror y
        try:
            self.task = nidaqmx.Task()
        except nidaqmx.DaqError as e:\
            print("An error occurred:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            self.task.close()


    def counter(self, sample_time):
        '''

        :param sample_time: sampling time for the connected single photon counter (milliseconds)
        :return: number of photon counts in one second
        '''
        self.task.ci_channels.add_ci_count_edges_chan(self.ctr_chan)
        self.task.ci_channels[0].ci_count_edges_term = self.photon_term

        self.task.start()
        time.sleep(sample_time)
        cnt0 = self.task.read()
        time.sleep(sample_time)

        cnt1 = self.task.read()
        self.task.stop()
        phot_cnt = (cnt1 - cnt0) * (sample_time) ** -1
        return phot_cnt

    def scan_voltage(self):
        pass

    def add_ai_channel(self, channel):
        self.task.ai_channels.add_ai_voltage_chan(channel)

    def read_analogue_voltage(self, channel="ai0", min=-10, max=10, rate=1000, n_samps=1):
        self.task.ai_channels.all.ai_min = min
        self.task.ai_channels.all.ai_max = max

        # Set the acquisition parameters
        self.task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

        # Start the acquisition
        self.task.start()
        data = self.task.read(number_of_samples_per_channel=n_samps)
        self.task.stop()
        return data
