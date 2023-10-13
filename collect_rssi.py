import csv
from datetime import datetime
from scapy.all import *
import time
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
duration = 5  # Number of seconds to sniff for
file_name = "collect_rssi2.csv"  # Name of CSV file where RSSI values are stored


def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    #header = ["date", "time", "dest", "src", "rssi"]
    header = ['RSSI', 'Timestamp']
    with open(file_name, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def captured_packet_callback(pkt):
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
    
    if os.path.isfile('collect_rssi2.csv'):
        with open('collect_rssi2.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([cur_dict['rssi'], time])
    else:
        with open('collect_rssi2.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['RSSI', 'Timestamp'])
            writer.writerow([cur_dict['rssi'], time])
                         # code here ###################

    # Only write the RSSI values of packets that are coming from your assigned transmitter (hint: filter by pkt.addr2, the destination MAC field)
    # Use the 'writerow' method to write the RSSI value and the current timestamp to the CSV file

    ######################################################


if __name__ == "__main__":
    create_rssi_file()

    t = AsyncSniffer(iface=iface_n, prn=captured_packet_callback, store=0)
    t.daemon = True
    t.start()
    
    start_date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f") #Get current date and time

    time.sleep(duration)
    t.stop()
    '''
    df = pd.read_csv("collect_rssi.csv", parse_dates=["timestamp"])
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["rssi"], label="RSSI")
    plt.xlabel("Time")
    plt.ylabel("RSSI (dBm)")
    plt.title("RSSI vs. Time")
    plt.legend()
    plt.grid(True)
    plt.show()
    '''

    print("Start Time: ", start_date_time)