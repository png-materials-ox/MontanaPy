# import pyqtgraph as pg
# import numpy as np
# import time
#
# x_waveform = [0.001 + i*0.0001 for i in range(11)]
# y_waveform = [0.001 + i*0.0001 for i in range(11)]
#
# app = pg.mkQApp("Plotting Example")
# win = pg.GraphicsLayoutWidget(show=True, title="Plotting Example")
# plot = win.addPlot()
# plot.setLabel('bottom', 'X Axis Label')
# plot.setLabel('left', 'Y Axis Label')
# plot.setTitle('Plot Title')
# plot.setLimits(xMin=min(x_waveform), xMax=max(x_waveform),
#                yMin=min(y_waveform), yMax=max(y_waveform))
#
# # initialize plot with the first point
# last_point = pg.ScatterPlotItem(
#     pos=[(y_waveform[0], x_waveform[0])],
#     brush=pg.mkBrush('r'),
#     pen=None,
#     size=10,
# )
# plot.addItem(last_point)
#
# for i in range(len(x_waveform)):
#     for j in range(len(y_waveform)):
#         plot.removeItem(last_point)
#         new_point = pg.ScatterPlotItem(
#             pos=[(y_waveform[j], x_waveform[i])],
#             brush=pg.mkBrush('r'),
#             pen=None,
#             size=10,
#         )
#         plot.addItem(new_point)
#         app.processEvents()
#         time.sleep(1)
#         # update last_point to be the new point
#         last_point = new_point

import pyqtgraph as pg
import numpy as np
import time

x_waveform = np.linspace(0.001, 0.002, 11)
y_waveform = np.linspace(0.001, 0.002, 11)

# Create plot
app = pg.mkQApp("Plotting Example")
win = pg.GraphicsLayoutWidget(show=True, title="Plotting Example")
win.resize(800, 600)
plot = win.addPlot(title="Plot Title")
plot.setLabel('bottom', 'X Axis Label')
plot.setLabel('left', 'Y Axis Label')
plot.setXRange(x_waveform[0], x_waveform[-1])
plot.setYRange(y_waveform[0], y_waveform[-1])
last_point = plot.plot([x_waveform[0]], [y_waveform[0]], pen=None, symbol='o', symbolPen='r')

# Update plot
for i in range(len(x_waveform)):
    for j in range(len(y_waveform)):
        last_point.setData(x=[x_waveform[j]], y=[y_waveform[i]])
        pg.QtGui.QGuiApplication.processEvents()
        time.sleep(0.1)
