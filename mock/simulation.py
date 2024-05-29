import random
import pygame
import math
from agent import Agent
from grid import Grid


class Simulation:
    def __init__(self, grid_width, grid_height, num_agents, obstacle_percentage, time=0, num_tasks = 10):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = Grid(grid_width, grid_height, obstacle_percentage)
        self.agents = []
        self.symbols = ['A', 'B', 'C', 'D', 'E']
        self.colors = [(255, 255, 255), (0, 255, 255), (0, 255, 0), (255, 255, 0), (255, 0, 255)]
        self.goal_colors = [(160, 160, 160), (0, 160, 160), (0, 160, 0), (160, 160, 0), (160, 0, 160)]
        self.num_tasks = num_tasks
        self.grid.add_obstacles()
        self.task_list = self.create_task_list()
        self.time_to_complete_tasks = time

        for i in range(num_agents):
            x, y = self.get_valid_goal_position()
            initial_task = self.task_list.pop()
            pickup_x, pickup_y = initial_task[0][0], initial_task[0][1]
            goal_x, goal_y = initial_task[1][0], initial_task[1][1]
            symbol = self.symbols[i]
            color = self.colors[i]
            goal_color = self.goal_colors[i]
            agent = Agent(x, y, goal_x, goal_y, pickup_x, pickup_y, symbol, color, goal_color)
            self.agents.append(agent)


    def create_task_list(self):
        # task: [pickup, goal]
        task_list = []
        for i in range(self.num_tasks):
            pickup_x, pickup_y = self.get_valid_goal_position()
            goal_x, goal_y = self.get_valid_goal_position()
            while pickup_x == goal_x and pickup_y == goal_y:
                goal_x, goal_y = self.get_valid_goal_position()

            task_list.append([[pickup_x, pickup_y], [goal_x, goal_y]])
        return task_list
    
    def give_new_task(self, agent):
        new_task = self.task_list.pop()
        agent.pickup_x, agent.pickup_y = new_task[0][0], new_task[0][1]
        agent.goal_x, agent.goal_y = new_task[1][0], new_task[1][1]
        agent.reached_goal = False
        agent.has_item = False

    def completed_all_tasks(self):
        if not self.task_list and False not in [agent.reached_goal for agent in self.agents]:
            return True

    def get_valid_goal_position(self):
        while True:
            goal_x, goal_y = random.randint(0, self.grid_width-1), random.randint(0, self.grid_height-1)
            if self.grid.is_empty(goal_x, goal_y, self.agents):
                return goal_x, goal_y
    
    def draw_grid(self, screen):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid.grid[y][x] == '#':
                    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(x*20, y*20, 20, 20))
        # Draw the grid lines
        for y in range(self.grid_height + 1):
            pygame.draw.line(screen, (110, 110, 110), (0, y * 20), (self.grid_width * 20, y * 20))
        for x in range(self.grid_width + 1):
            pygame.draw.line(screen, (110, 110, 110), (x * 20, 0), (x * 20, self.grid_height * 20))
    
    def draw_agents(self, screen):
        for agent in self.agents:
            font = pygame.font.SysFont(None, 20)
            text_surface = font.render(agent.symbol, True, agent.color)
            screen.blit(text_surface, (agent.x*20 + 5, agent.y*20 + 9))
            if agent.has_item:
                pygame.draw.circle(screen, agent.goal_color, (agent.x*20 + 10, agent.y*20 + 5), 5)
            if not agent.has_item:
                pygame.draw.circle(screen, agent.goal_color, (agent.pickup_x*20 + 10, agent.pickup_y*20 + 5), 5)
            pygame.draw.rect(screen, agent.goal_color, pygame.Rect(agent.goal_x*20, agent.goal_y*20, 20, 20), width=1)
    
    def update_agents(self):
        for agent in self.agents:
            agent.move(self.grid, self.agents)
            if agent.reached_goal:
                if self.task_list:
                    self.give_new_task(agent)