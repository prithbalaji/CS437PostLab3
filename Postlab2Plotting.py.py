# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YsJQMf02XawuknNU5lyXn7IpAU4T14H-
"""

import numpy as np
import time
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd


## Install the following libraries if they are not already installed on your Raspi:
## pip3 install seaborn
## sudo apt-get install python3-pandas
## sudo apt-get install python3-matplotlib



filename="sample_data/smoothed_01_54_05.csv"

## CSV file template:
# time in seconds, timestamp (H:M:S), X-Acceleration, Y-Acceleration, Z-Acceleration, X-Gyroscope, Y-Gyro,Z-Gyro, X-Gyro, Y-Gyro, Z-gyro


df =pd.read_csv(filename, header=None)

#df=df.dropna()
print(df)
cmap = plt.get_cmap('viridis')


x = df[0][1:]

dt = 0.7
x = [float(i) for i in x]
print("xx", x)
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
plt.xlim(-2,5)

# Set y-axis limits
plt.ylim(-2, 5)

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

!pip install scip[y]

import numpy as np
import time
import scipy.signal as signal
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd

import seaborn as sns # visualization






filename="sample_data/22_39_41.csv"

## CSV file template:
# time in seconds, timestamp (H:M:S), X-Acceleration, Y-Acceleration, Z-Acceleration, X-Gyroscope, Y-Gyro,Z-Gyro, X-Gyro, Y-Gyro, Z-gyro



df =pd.read_csv(filename, header=None)
df=df.dropna()

timestamp = df[0]
x_axis=df[2][1:]
y_axis=df[3][1:]
z_axis=df[4][1:]


x_axis = [float(i) for i in x_axis]
y_axis = [float(i) for i in y_axis]
z_axis = [float(i) for i in z_axis]

## Visualize your Accelerometer Values
plt.plot(x_axis)
plt.plot(y_axis)
plt.plot(z_axis)
plt.show()



## CALIBERATION
# caliberate x,y,z to reduce the bias in accelerometer readings. Subtracting it from the mean means that in the absence of motion, the accelerometer reading is centered around zero to reduce the effect of integrigation drift or error.
# change the upper and lower bounds for computing the mean where the RPi is in static position at the begining of the experiment (i.
print(type(x_axis), "YTFGJKBNML")
print(x_axis[2], type(x_axis[2]))
x_calib_mean = np.mean(x_axis[1:50])
x_calib = x_axis - x_calib_mean
x_calib = x_calib[:]
timestamp = timestamp[:]

y_calib_mean = np.mean(y_axis[1:50])
y_calib = y_axis - y_calib_mean
y_calib = y_calib[:]
timestamp = timestamp[:]

z_calib_mean = np.mean(z_axis[1:50])
z_calib = z_axis - z_calib_mean
z_calib = z_calib[:]
timestamp = timestamp[:]



plt.plot(x_calib)
plt.plot(y_calib[10:])
plt.plot(z_axis)

plt.show()

accel_raw = np.linalg.norm(np.array([x_calib, y_calib, z_calib]), axis=0)
accel = signal.savgol_filter(accel_raw, window_length=11, polyorder=4) ## Same as rolling average --> Savitzky-Golay smoothing
## change the window size as it seems fit. If you keep window size too high it will not capture the relevant peaks/steps

# Plot the original and smoothed data
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(accel_raw)
plt.title("Original Data")
plt.subplot(2, 1, 2)
plt.plot(accel)
plt.title("Smoothed Data")
plt.show()


## Step Detection: The instantaneous peaks in the accelerometer readings correspond to the steps. We use thresholding technique to decide the range of peak values for step detection
# Set a minimum threshold (e.g., 1.0) for peak detection
min_threshold = 0.1  ## Change the threshold (if needed) based on the peak accelerometer values that you observe in your plot above

# Calculate the upper threshold for peak detection as the maximum value in the data
upper_threshold = np.max(accel)

# Define the range for peak detection
my_range = (min_threshold, upper_threshold)

# print("range of Accel. values  for peak detection",my_range)
## Visualize the detected peaks in the accelerometer readings based on the selected range
plt.plot(accel)
peak_array, _ = signal.find_peaks(accel, height=my_range, distance=5)
plt.plot(peak_array, accel[peak_array], "x", color="r")
plt.show()

print("Accel values at high peaks-->", accel[peak_array])

print("Peak array indices are", peak_array)

# Extract  the timestamps corresponding to detected peaks
timestamp_for_peaks = df[1][peak_array]

# Create a new DataFrame with timestamp and peak values
peaks_df = pd.DataFrame({'Timestamp': timestamp_for_peaks, 'PeakValue': accel[peak_array]})
print("Peaks_df is", peaks_df)

# Set the orientation/direction of motion (walking direction).
# walking_direction is an angle in degrees with global frame x-axis. It can be from 0 degrees to 360 degrees.
# for e.g. if walking direction is 90 degrees, user is walking in the positive y-axis direction.
# Assuming you are moving along the +X-axis with minor deviations/drifts in Y, we set the orientation to 5 (ideally it should be 0 but to take into account the drifts we keep 5)
# Additionally, we assume that the walking direction will be the same throught the trajectory that you capture in this exercise.
walking_dir = np.deg2rad(5) ## deg to radians





# To compute the step length, we estimate it to be propertional to the height of the user.
height=1.75 # in meters
step_length= 0.415 * height # in meters

# Convert walking direction into a 2D unit vector representing motion in X, Y axis:
angle = np.array([np.cos(walking_dir), np.sin(walking_dir)])


## Start position of the user i.e. (0,0)
cur_position = np.array([0.0, 0.0], dtype=float)
t = []
for i in range(len(peaks_df)):
    t.append(cur_position)

    cur_position = cur_position + step_length * angle

t = np.array(t)
print("Trajectory positions are---------------------------->", t)
