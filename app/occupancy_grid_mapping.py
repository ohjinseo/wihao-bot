import numpy as np

def occupancy_grid_mapping(laser_ranges, robot_pose, grid_map):

    map_width, map_height = grid_map.shape
    resolution = 0.1  
    
    # 로봇 위치 및 방향
    robot_x, robot_y, robot_theta = robot_pose
    
    max_range = 30.0 
    
    # 레이저 스캔 각도 범위
    angle_min = -np.pi / 2 
    angle_max = np.pi / 2   
    
    # 셀 단위 변화량 계산
    dx = resolution * np.cos(robot_theta)
    dy = resolution * np.sin(robot_theta)
    
    # 로봇의 현재 위치를 맵 좌표로 변환
    robot_map_x = int(robot_x / resolution)
    robot_map_y = int(robot_y / resolution)
    
    # 맵을 순회하며 레이저 스캔 결과 반영
    for i in range(len(laser_ranges)):
        range_i = laser_ranges[i]
        angle_i = angle_min + i * (angle_max - angle_min) / len(laser_ranges)
        
        obstacle_x = robot_x + range_i * np.cos(robot_theta + angle_i)
        obstacle_y = robot_y + range_i * np.sin(robot_theta + angle_i)
        
        obstacle_map_x = int(obstacle_x / resolution)
        obstacle_map_y = int(obstacle_y / resolution)

        if obstacle_map_x < 0 or obstacle_map_x >= map_width or \
           obstacle_map_y < 0 or obstacle_map_y >= map_height:
            continue

        if range_i < max_range:
            grid_map[robot_map_x:obstacle_map_x, robot_map_y:obstacle_map_y] += 1
        else:
            grid_map[obstacle_map_x, obstacle_map_y] += 1
    
    return grid_map