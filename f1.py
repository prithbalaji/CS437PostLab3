import numpy as np
import time
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd


## Install the following libraries if they are not already installed on your Raspi:
## pip3 install seaborn
## sudo apt-get install python3-pandas
## sudo apt-get install python3-matplotlib



filename="sample_data/21_15_57.csv"

## CSV file template:
# time in seconds, timestamp (H:M:S), X-Acceleration, Y-Acceleration, Z-Acceleration, X-Gyroscope, Y-Gyro,Z-Gyro, X-Gyro, Y-Gyro, Z-gyro


df =pd.read_csv(filename, header=None)
df=df.dropna()

cmap = plt.get_cmap('viridis')


x = df[0][1:]
dt = 0.7
x = [float(i) for i in x]
x_calib = (np.array(x)-np.array(x).mean()).tolist()

## caliberate x,y,z to reduce the bias in accelerometer readings. Subtracting it from the mean means that in the absence of motion, the accelerometer reading is centered around zero to reduce the effect of integrigation drift or error.
## change the upper and lower bounds for computing the mean where the RPi is in static position at the begining of the experiment (i.e. for the first few readings). You can know these bounds from the exploratory plots above.
# x_calib = x - x_calib
# x_calib = x_calib[:]
x_vel = [0]
for i in range(len(x_calib)-1):
    x_vel.append(x_vel[-1] + dt * x_calib[i])
x = [0]

for i in range(len(x_vel)-1):
    x.append(x[-1] + dt * x_vel[i])


y = df[1][1:]
y = [float(i) for i in y]
y_calib = (np.array(y)-np.array(y).mean()).tolist()
print(y_calib)
y_vel = [0]
for i in range(len(y_calib)-1):
    y_vel.append(y_vel[-1] + dt * y_calib[i])

y = [0]

for i in range(len(y_vel)-1):
    y.append(y[-1] + dt * y_vel[i])
y = [abs(y_val) for y_val in y]

rssi = df[2][1:]

rssi_int = [float(rs) for rs in rssi]

print(rssi_int)
print("x", y)
plt.scatter(x, y, c=rssi_int, cmap='viridis', alpha=0.7)
plt.colorbar(label='RSSI') 

# norm = plt.Normalize(min(rssi_int), max(rssi_int))
# scalar_map = plt.cm.ScalarMappable(cmap = cmap, norm = norm)
# colors = [scalar_map.to_rgba(num) for num in rssi_int]
# timestamp = df[3]

# plt.scatter(x, y, c = rss, cmap = 'viridis', s=20)
# plt.show()

plt.xlabel("X-axis")
plt.ylabel("Y-label")
plt.xlim(-10,10)

# Set y-axis limits
plt.ylim(-7, 7)

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
