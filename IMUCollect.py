from sense_hat import SenseHat
import numpy as np
import time
import scipy.signal as signal
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd

import scipy.integrate as integrate
path="/home/pi/Desktop/lab3/IMU/newdata/"
sense=SenseHat()

timestamp_fname=datetime.now().strftime("%H:%M:%S")
sense.set_imu_config(True,True,True) ## Config the Gyroscope, Accelerometer, Magnetometer
filename=path+timestamp_fname+".csv"

with open(filename,"a") as f:
    while True:
        accel=sense.get_accelerometer_raw()  ## returns float values representing acceleration intensity in Gs
        gyro=sense.get_gyroscope_raw()  ## returns float values representing rotational intensity of the axis in radians per second
        mag=sense.get_compass_raw()  ## returns float values representing magnetic intensity of the ais in microTeslas
        
        x=accel['x']
  
        y=accel['y']
        z=accel['z']
        timestamp=datetime.now().strftime("%H:%M:%S")
        entry= str(time.time())+","+timestamp+","+str(x)+","+str(y)+","+str(z)+","+ str(gyro['x'])+ ","+str(gyro['y'])+","+ str(gyro['z'])+ ","+ str(mag['x'])+ ","+str(mag['y'])+","+ str(mag['z'])+"\n"
    
    

        
        f.write(entry)
   
        
f.close()
        


