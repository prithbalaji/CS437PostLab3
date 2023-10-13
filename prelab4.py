from sense_hat import SenseHat
import time
import math

sense = SenseHat()

while True:

    accel = sense.get_accelerometer_raw()
    mag = sense.get_compass_raw()


    pitch = math.atan2(accel['x'], math.sqrt(accel['y']**2 + accel['z']**2))
    roll = math.atan2(accel['y'], math.sqrt(accel['x']**2 + accel['z']**2))
    yaw = math.atan2(mag['y'], mag['x'])

    
    pitch = math.degrees(pitch)
    roll = math.degrees(roll)
    yaw = math.degrees(yaw)

     
    yaw += 90.0  

    
    print(f"Pitch: {pitch:.2f} degrees")
    print(f"Roll: {roll:.2f} degrees")
    print(f"Yaw: {yaw:.2f} degrees")
    print(accel['x'])
    print(accel['y'])
    print(accel['z'])

    
    time.sleep(0.1)

