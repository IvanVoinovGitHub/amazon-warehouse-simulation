from gui import Gui

def main():
    game_configs = {"game_configs": [{"grid_width": 30, "grid_height": 30, "num_agents": 5, "obstacle_percentage": 1, "time": 0, "num_tasks": 30}, 
                                     {"grid_width": 20, "grid_height": 20, "num_agents": 3, "obstacle_percentage": 5, "time": 0, "num_tasks": 10}, 
                                     {"grid_width": 30, "grid_height": 30, "num_agents": 2, "obstacle_percentage": 10, "time": 20, "num_tasks": 20}]}
    input_window = Gui(game_configs)

if __name__ == "__main__":
    main()
