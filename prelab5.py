from sense_hat import SenseHat
import time
import csv
import matplotlib.pyplot as plt


sense = SenseHat()
timestamps = []
raw_x_values = []
raw_y_values = []
raw_z_values = []
smoothed_x_values = []
smoothed_y_values = []
smoothed_z_values = []


window_size = 10
window_values = [0] * window_size  


try:
    while True:
        
        accel = sense.get_accelerometer_raw()
        x = accel['x']
        y = accel['y']
        z = accel['z']

        
        timestamp = time.time()

        
        timestamps.append(timestamp)
        raw_x_values.append(x)
        raw_y_values.append(y)
        raw_z_values.append(z)

        
        window_values.pop(0) 
        window_values.append(x)
        smoothed_x = sum(window_values) / window_size

        window_values.pop(0)
        window_values.append(y)
        smoothed_y = sum(window_values) / window_size

        window_values.pop(0)
        window_values.append(z)
        smoothed_z = sum(window_values) / window_size

        smoothed_x_values.append(smoothed_x)
        smoothed_y_values.append(smoothed_y)
        smoothed_z_values.append(smoothed_z)

        
        time.sleep(0.1)

except KeyboardInterrupt:
    # Save data to a CSV file when interrupted
    with open('accelerometer_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Raw X', 'Raw Y', 'Raw Z', 'Smoothed X', 'Smoothed Y', 'Smoothed Z'])
        for i in range(len(timestamps)):
            writer.writerow([timestamps[i], raw_x_values[i], raw_y_values[i], raw_z_values[i],
                             smoothed_x_values[i], smoothed_y_values[i], smoothed_z_values[i]])

    # Create plots
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(timestamps, raw_x_values, label='Raw X')
    plt.plot(timestamps, raw_y_values, label='Raw Y')
    plt.plot(timestamps, raw_z_values, label='Raw Z')
    plt.title('Raw Accelerometer Readings')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(timestamps, smoothed_x_values, label='Smoothed X')
    plt.plot(timestamps, smoothed_y_values, label='Smoothed Y')
    plt.plot(timestamps, smoothed_z_values, label='Smoothed Z')
    plt.title('Smoothed Accelerometer Readings (Moving Average)')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()

    plt.tight_layout()
    plt.show()
