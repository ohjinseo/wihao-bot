import time
import occupancy_grid_mapping
import a_star
import lidar

start_x, start_y = map(int, input("Enter start coordinates (x, y): ").split())
goal_x, goal_y = map(int, input("Enter goal coordinates (x, y): ").split())
start = (start_x, start_y)
goal = (goal_x, goal_y)

while True:
    laser_ranges = lidar()

    grid_map = occupancy_grid_mapping(laser_ranges, robot_pose, grid_map)

    path = a_star(start, goal, grid_map)

    if path:
        for waypoint in path:
            print(f"Moving to {waypoint}")
            time.sleep(1) 
    else:
        print("No path to goal. Exiting.")
        break