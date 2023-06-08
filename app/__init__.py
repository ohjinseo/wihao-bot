import numpy as np
import serial

lidar_port = "/dev/ttyUSB0" 
lidar_baudrate = 115200  
lidar_serial = serial.Serial(lidar_port, lidar_baudrate)

map_size = (100, 100)  
map_resolution = 0.1  
occupancy_map = np.zeros(map_size, dtype=np.int8)  # Occupancy Grid Map 초기화

robot_pose = (map_size[0] // 2 * map_resolution, map_size[1] // 2 * map_resolution, 0)