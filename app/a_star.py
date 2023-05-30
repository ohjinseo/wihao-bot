import numpy as np
import heapq

def heuristic_cost_estimate(start, goal):
    return np.linalg.norm(goal - start)

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def a_star(start, goal, grid_map):
    map_width, map_height = grid_map.shape
    
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0, start))
    
    g_score = {start: 0}
    h_score = {start: heuristic_cost_estimate(start, goal)}
    
    f_score = {start: h_score[start]}
    
    came_from = {}
    
    while open_list:
        current = heapq.heappop(open_list)[1]
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        closed_list.add(current)
        
        neighbors = []
        x, y = current
        if x > 0:
            neighbors.append((x - 1, y))
        if x < map_width - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < map_height - 1:
            neighbors.append((x, y + 1))
        
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1
            
            if grid_map[neighbor] > 0:
                continue

            if neighbor in closed_list:
                continue
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                h_score[neighbor] = heuristic_cost_estimate(neighbor, goal)
                f_score[neighbor] = g_score[neighbor] + h_score[neighbor]
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None