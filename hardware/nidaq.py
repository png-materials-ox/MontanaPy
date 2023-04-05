import nidaqmx
import time

class DAQ:
    def __init__(self):

        #TODO get from config file
        self.dev = "Dev1"
        self.ctr_chan = self.dev + "/ctr0"
        self.ctr_term = "/" + self.dev + "/PFI8"

    def counter(self, sample_time):
        try:
            with nidaqmx.Task() as task:
                task.ci_channels.add_ci_count_edges_chan(self.ctr_chan)
                task.ci_channels[0].ci_count_edges_term = self.ctr_term

                task.start()
                time.sleep(sample_time)
                cnt0 = task.read()
                time.sleep(sample_time)

                cnt1 = task.read()
                task.stop()
                p = (cnt1 - cnt0) * (sample_time) ** -1
                return p
        except nidaqmx.DaqError as e:\
            print("An error occurred:", e)

        except Exception as e:
            print("An unexpected error occurred:", e)

        finally:
            task.close()