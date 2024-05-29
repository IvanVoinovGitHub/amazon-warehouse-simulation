import time
import pygame
import tkinter as tk
from tkinter import messagebox
from simulation import Simulation


class Gui:
    def __init__(self, game_configs=None):
        if game_configs:
            for game_config in game_configs["game_configs"]:
                self.start_simulation(game_config["grid_width"], 
                                        game_config["grid_height"], 
                                        game_config["num_agents"], 
                                        game_config["obstacle_percentage"], 
                                        game_config["time"],
                                        game_config["num_tasks"])
        else:
            self.root = tk.Tk()
            self.root.title("Input")
            self.root.geometry("300x200")
            
            self.label1 = tk.Label(self.root, text="Grid Width:")
            self.label1.pack()
            self.entry1 = tk.Entry(self.root)
            self.entry1.pack()
            
            self.label2 = tk.Label(self.root, text="Grid Height:")
            self.label2.pack()
            self.entry2 = tk.Entry(self.root)
            self.entry2.pack()
            
            self.label3 = tk.Label(self.root, text="Number of Agents:")
            self.label3.pack()
            self.entry3 = tk.Entry(self.root)
            self.entry3.pack()
            
            self.label4 = tk.Label(self.root, text="Obstacle Percentage:")
            self.label4.pack()
            self.entry4 = tk.Entry(self.root)
            self.entry4.pack()
        
            self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
            self.submit_button.pack()
            
            self.root.mainloop()
        
    def submit(self):
        grid_width = int(self.entry1.get())
        grid_height = int(self.entry2.get())
        num_agents = int(self.entry3.get())
        obstacle_percentage = int(self.entry4.get())
        if grid_width < 10 or grid_width > 100 or grid_height < 10 or grid_height > 100:
            messagebox.showerror("Error", "Grid dimensions must be between 10 and 100.")
            return
        if num_agents < 2 or num_agents > 5:
            messagebox.showerror("Error", "Number of agents must be between 2 and 5.")
            return
        if obstacle_percentage < 0 or obstacle_percentage > 100:
            messagebox.showerror("Error", "Obstacle percentage must be between 0 and 100.")
            return
        self.root.destroy()
        self.start_simulation(grid_width, grid_height, num_agents, obstacle_percentage, time)
    
    def start_simulation(self, grid_width, grid_height, num_agents, obstacle_percentage, time, num_tasks):
        simulation = Simulation(grid_width, grid_height, num_agents, obstacle_percentage, time, num_tasks)
        self.run_simulation(simulation)
    
    def run_simulation(self, simulation):
        pygame.init()
        screen = pygame.display.set_mode((simulation.grid_width*20, simulation.grid_height*20))
        pygame.display.set_caption("Agent Simulation")
        clock = pygame.time.Clock()
        
        if simulation.time_to_complete_tasks == 0:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                screen.fill((0, 0, 0))
                simulation.draw_grid(screen)
                simulation.draw_agents(screen)
                simulation.update_agents()
                # Need to check which agents have completed their task
                pygame.display.flip()
                clock.tick(5)  # Adjust the speed of the simulation here
            print("Initial number of tasks:" + str(simulation.num_tasks))
            print("Tasks completed:" + str(simulation.num_tasks - len(simulation.task_list)))
            pygame.quit()
        else:
            start_time = time.time()
            end_time = start_time + simulation.time_to_complete_tasks
            while time.time() < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                screen.fill((0, 0, 0))
                simulation.draw_grid(screen)
                simulation.draw_agents(screen)
                simulation.update_agents()
                # Need to check which agents have completed their task
                pygame.display.flip()
                clock.tick(5)  # Adjust the speed of the simulation here
            print("Initial number of tasks:" + str(simulation.num_tasks))
            print("Number of tasks completed in " + str(simulation.time_to_complete_tasks) + " seconds: " + str(simulation.num_tasks - len(simulation.task_list)))
            pygame.quit()
            

