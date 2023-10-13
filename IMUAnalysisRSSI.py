import numpy as np
import time
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd


## Install the following libraries if they are not already installed on your Raspi:
## pip3 install seaborn
## sudo apt-get install python3-pandas
## sudo apt-get install python3-matplotlib



filename="/home/pi/Desktop/lab3/IMU/newdata/left_rssi.csv"

## CSV file template:
# time in seconds, timestamp (H:M:S), X-Acceleration, Y-Acceleration, Z-Acceleration, X-Gyroscope, Y-Gyro,Z-Gyro, X-Gyro, Y-Gyro, Z-gyro


df =pd.read_csv(filename, header=None)
df=df.dropna()

cmap = plt.get_cmap('viridis')


x_axis = df[0][1:]
y_axis = df[1][1:]
rssi = df[2][1:]
rssi_int = [abs(int(rs)) for rs in rssi]
print(rssi_int)
norm = plt.Normalize(min(rssi_int), max(rssi_int))
scalar_map = plt.cm.ScalarMappable(cmap = cmap, norm = norm)
colors = [scalar_map.to_rgba(num) for num in rssi_int]
timestamp = df[3]

plt.scatter(x_axis, y_axis, c = colors, cmap = 'viridis', s=20)
plt.show()

'''
plt.plot(x_axis,  label="X-axis Raw Acceleration")
plt.plot(y_axis,  label="Y-axis Raw Acceleration")
#plt.plot(z_axis,  label="Z-axis Raw Acceleration")
plt.plot(rssi,  label="RSSI")
plt.legend(loc="upper left")
plt.ylabel("Raw Acceleration in m/s^2")
plt.xlabel("Number of Data Points")
'''
