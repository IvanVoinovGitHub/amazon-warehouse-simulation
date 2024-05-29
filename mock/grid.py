import random
from collections import deque


class Grid:
    def __init__(self, width, height, obstacle_percentage):
        self.width = width
        self.height = height
        self.obstacle_percentage = obstacle_percentage
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    def add_obstacles(self):
        num_obstacles = int(self.width * self.height * self.obstacle_percentage / 100)
        for _ in range(num_obstacles):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self.grid[y][x] = '#'

    
    def is_valid_move(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_empty(self, x, y, agents):
        return self.grid[y][x] != '#' and not any(agent.x == x and agent.y == y for agent in agents) 