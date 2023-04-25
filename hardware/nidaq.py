import nidaqmx
from nidaqmx.constants import (
    Edge,
    AcquisitionType,
    Signal,
    VoltageUnits)
import time
import json
import os
import contextlib


class DAQ:
    def __init__(self):
        conf_path = os.path.join(os.getcwd() + "\\config\\config.json")

        with self._open_config(conf_path) as config:
            self.daq = config["hardware"]["nicard"]        # Daq device ID

        self.ctr_chan = self.daq["counter_channels"][0]     # DAQ channel for single photon counting
        self.photon_term = self.daq["photon_sources"][0]    # Associated timing channel for single photon counting

        self.fsm_x_chan_o = self.daq["scan_x"]
        self.fsm_y_chan_o = self.daq["scan_y"]

    @contextlib.contextmanager
    def _open_task(self):
        """
            A context manager that creates a new nidaqmx.Task object and yields it, and then
            closes the Task object after the block of code in the with statement completes. If an
            exception occurs inside the with block, the exception is caught and printed before the
            Task object is closed.

            :return: A new nidaqmx.Task object.
            :rtype: nidaqmx.Task
            """
        try:
            task = nidaqmx.Task()
            yield task
        except nidaqmx.errors.DaqError() as e:
            print(e)
        finally:
            task.close()

    @contextlib.contextmanager
    def _open_config(self, filepath):
        """
            A context manager that opens a JSON configuration file at the specified filepath, loads
            its contents into a Python dictionary, and yields the dictionary to the calling code. If
            an error occurs during the process, the error is caught and printed to the console. The
            file is always closed after the with block completes.

            :param filepath: The filepath of the JSON configuration file to open.
            :type filepath: str

            :return: A dictionary containing the contents of the JSON configuration file.
            :rtype: dict
            """
        try:
            with open(filepath, 'r') as file:
                yield json.load(file)
                # return data
        except Exception as e:
            print(f"Error: {e}")
        finally:
            file.close()

    def counter(self, sample_time):
        '''

        :param sample_time: sampling time for the connected single photon counter (milliseconds)
        :return: number of photon counts in one second
        '''
        try:
            with nidaqmx.Task() as task:
                task.ci_channels.add_ci_count_edges_chan(self.ctr_chan)
                task.ci_channels[0].ci_count_edges_term = self.photon_term

                task.start()
                time.sleep(sample_time)
                cnt0 = task.read()
                time.sleep(sample_time)

                cnt1 = task.read()
                task.stop()
                phot_cnt = (cnt1 - cnt0) * (sample_time) ** -1
                return phot_cnt
        except nidaqmx.DaqError as e:\
            print("An error occurred:", e)

        except Exception as e:
            print("An unexpected error occurred:", e)

        finally:
            task.close()

    def scan_voltage(self):
        pass

    def scan_xy(self, x_waveform=[], y_waveform=[], dwell_ms=10):
        """
            Generates a two-dimensional waveform using the x and y waveform inputs and scans it using
            the nidaqmx.Task object in a finite acquisition mode. The function opens the Task
            object using the _open_task context manager and configures the analog output channels for
            the x and y channels. It sets the sample clock rate and total number of samples for the
            acquisition, writes the waveform to the Task object, and starts the acquisition. The
            acquisition is then stopped and the Task object is closed.

            :param x_waveform:  A list of values representing the x-axis waveform to be generated and
                                scanned.
            :type x_waveform:   list

            :param y_waveform:  A list of values representing the y-axis waveform to be generated and
                                scanned.
            :type y_waveform:   list

            :param x_rate: The sampling rate for the x-axis waveform in Hz.
            :type x_rate: float

            :param y_rate: The sampling rate for the y-axis waveform in Hz.
            :type y_rate: float

            :raises ValueError: If the length of the x_waveform and y_waveform arrays are not the same.

            :return: None
            """
        with self._open_task() as task:
            task.ao_channels.add_ao_voltage_chan(self.fsm_x_chan_o)
            task.ao_channels.add_ao_voltage_chan(self.fsm_y_chan_o)
            task.ao_channels.all.ao_max = 10 #TODO put in config file
            task.ao_channels.all.ao_min = -10

            # task.timing.cfg_samp_clk_timing(
            #     rate=max(x_rate, y_rate),
            #     sample_mode=AcquisitionType.FINITE,
            #     samps_per_chan=len(x_waveform) + len(y_waveform)
            # )

            task.start()
            for i in range(len(x_waveform)):
                for j in range(len(y_waveform)):
                    task.write(
                        [x_waveform[i], y_waveform[j]],
                        auto_start=False
                    )
                    time.sleep(dwell_ms/1000)

            task.stop()
            task.wait_until_done(timeout=nidaqmx.constants.WAIT_INFINITELY)

    def set_ao_voltage(self, channel, voltage):
        """
        """
        with self._open_task() as task:
            task.ao_channels.add_ao_voltage_chan(channel)
            task.ao_channels.all.ao_max = 10 #TODO put in config file
            task.ao_channels.all.ao_min = -10

            task.start()
            task.write([voltage],auto_start=False)

            task.stop()
            task.wait_until_done(timeout=nidaqmx.constants.WAIT_INFINITELY)

    def read_analogue_voltage(self, channels=["ai0", "ai1"], min=-10, max=10, rate=1000, n_samps=1):
        # Create a DAQ session
        with nidaqmx.Task() as task:
            # Configure the input channels
            for channel in channels:
                task.ai_channels.add_ai_voltage_chan(channel)

            task.ai_channels.all.ai_min = min
            task.ai_channels.all.ai_max = max

            # Set the acquisition parameters
            task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Start the acquisition
            task.start()
            data = task.read(number_of_samples_per_channel=n_samps)
            task.stop()
            return data
