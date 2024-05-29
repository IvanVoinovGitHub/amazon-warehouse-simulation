import random


class Agent:
    def __init__(self, x, y, goal_x, goal_y, pickup_x, pickup_y, symbol, color, goal_color):
        self.x = x
        self.y = y
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.pickup_x = pickup_x
        self.pickup_y = pickup_y
        self.symbol = symbol
        self.color = color
        self.goal_color = goal_color
        self.reached_goal = False
        self.has_item = False
    
    def move(self, grid, agents):
        if not self.reached_goal:
            possible_moves = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = self.x + dx, self.y + dy
                if grid.is_valid_move(new_x, new_y) and grid.is_empty(new_x, new_y, agents):
                    possible_moves.append((new_x, new_y))
            
            if possible_moves:
                random.shuffle(possible_moves)  # Randomly shuffle the list of possible moves
                if self.has_item:
                    distances = [abs(move[0] - self.goal_x) + abs(move[1] - self.goal_y) for move in possible_moves]
                else:
                    distances = [abs(move[0] - self.pickup_x) + abs(move[1] - self.pickup_y) for move in possible_moves]
                min_distance_index = distances.index(min(distances))
                self.x, self.y = possible_moves[min_distance_index]
            
            # Check if the agent has reached its goal state
            if not self.has_item and self.x == self.pickup_x and self.y == self.pickup_y:
                self.has_item = True
            elif self.has_item and self.x == self.goal_x and self.y == self.goal_y:
                self.reached_goal = True