import numpy as np
import time
import nidaqmx
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# # Create plot
# fig, ax = plt.subplots()
# ax.set_xlabel('Time (s)')
# ax.set_ylabel('Count')
#
# # Initialize plot data
# x_data = []
# y_data = []
# line, = ax.plot(x_data, y_data)
#
# time_total = 0
#
# while True:
#     try:
#         with nidaqmx.Task() as task:
#             task.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")
#             task.ci_channels[0].ci_count_edges_term = "/Dev1/PFI8"
#
#             ts = 0.01
#
#             task.start()
#             for total_block in range(int(1/ts)):
#                 cnt = task.read()
#                 # time.sleep(0.0001)
# #                 plt.show();
#             print(cnt)
#             x_data.append(time_total)
#             y_data.append(cnt)
#             line.set_data(x_data, y_data)
#             ax.relim()
#             ax.autoscale_view()
#             plt.draw()
#             plt.pause(0.001)
#             time_total = time_total + ts
#
#     except nidaqmx.DaqError as e:
#         print("An error occurred:", e)
#
#     except Exception as e:
#         print("An unexpected error occurred:", e)
#
#     finally:
#         task.close()

import numpy as np
import time
import nidaqmx
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings("ignore")

# Create plot
fig, ax = plt.subplots()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Count')

# Initialize plot data
x_data = []
y_data = []
line, = ax.plot(x_data, y_data)

time_total = 0

while True:
    try:
        with nidaqmx.Task() as task:
            task.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")
            task.ci_channels[0].ci_count_edges_term = "/Dev1/PFI8"

            task.start()
            time.sleep(0.01)
            cnt0 = task.read()
            time.sleep(0.01)

            cnt1 = task.read()
            task.stop()
            p = (cnt1 - cnt0) * (0.01) ** -1

            time_total = time_total + .01
            x_data.append(time_total)
            y_data.append(p)
            line.set_xdata(x_data)
            line.set_ydata(y_data)
            ax.relim()
            ax.autoscale_view()

            plt.draw()
            plt.pause(0.001)
    except nidaqmx.DaqError as e:
        print("An error occurred:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

    finally:
        task.close()

