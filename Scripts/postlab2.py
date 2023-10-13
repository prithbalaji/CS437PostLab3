import csv
from datetime import datetime
from scapy.all import *
import time
from sense_hat import SenseHat
import os
#import pandas as pd
import matplotlib.pyplot as plt

"""
Run monitor_mode.sh first to set up the network adapter to monitor mode and to
set the interface to the right channel.
To get RSSI values, we need the MAC Address of the connection 
of the device sending the packets.
"""

# Variables to be modified
dev_mac = ""  # Assigned transmitter MAC
iface_n = "wlan1"  # Interface for network adapter
duration = 30  #1Number of seconds to sniff for
#file_name = "new.csv"  # Name of CSV file where RSSI values are stored

sense=SenseHat()
path="/home/pi/Desktop/lab3/IMU/newdata/"
timestamp_fname=datetime.now().strftime("%H:%M:%S")
sense.set_imu_config(True,True,True) ## Config the Gyroscope, Accelerometer, Magnetometer
filename=path+timestamp_fname+".csv"

max_rssi = (0,0,-1000)

def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    #header = ["date", "time", "dest", "src", "rssi"]
    header = ['x','y', 'RSSI', 'Timestamp']
    with open(filename, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def captured_packet_callback(pkt):
    global max_rssi
    """Save MAC addresses, time, and RSSI values to CSV file if MAC address of src matches"""
    missed_count = 0  # Number of missed packets while attempting to write to file
    cur_dict = {}

    try:
        
        cur_dict["mac_1"] = pkt.addr1
        cur_dict["mac_2"] = pkt.addr2
        cur_dict["rssi"] = pkt.dBm_AntSignal
    except AttributeError:
        return  # Packet formatting error

    
    date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f").split(",") #Get current date and time
    date = date_time[0]
    time = date_time[1]
    
    accel=sense.get_accelerometer_raw()  ## returns float values representing acceleration intensity in Gs
    gyro=sense.get_gyroscope_raw()  ## returns float values representing rotational intensity of the axis in radians per second
    mag=sense.get_compass_raw()  ## returns float values representing magnetic intensity of the ais in microTeslas

    x=accel['x']

    y=accel['y']
    z=accel['z']
   # print("cur d-", cur_dict)
    #if cur_dict['mac_1'] == 'e4:5f:01:d4:9f:f9'
    new_tuple = (x, y, cur_dict['rssi'])
    if cur_dict['mac_2'] == "e4:5f:01:d4:9c:b1":# or cur_dict['mac_1'] =="e4:5f:01:d4:9c:b1":
        if new_tuple[2] > max_rssi[2]:
            max_rssi = new_tuple
            print("NEW RSSI: ", max_rssi)
        print(cur_dict['rssi'],cur_dict['mac_1'],cur_dict['mac_2'])
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['x', 'y', 'RSSI'])
            writer.writerow([x, y, cur_dict['rssi']])

    timestamp=datetime.now().strftime("%H:%M:%S")

        

if __name__ == "__main__":
    create_rssi_file()
    t = AsyncSniffer(iface=iface_n, prn=captured_packet_callback, store=0)
    t.daemon = True
    t.start()
    
    start_date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f") #Get current date and time

    time.sleep(duration)
    t.stop()

    print("Start Time: ", start_date_time)
