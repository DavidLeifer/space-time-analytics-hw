import random

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid, MultiGrid, ContinuousSpace #might have to edit this
from mesa.time import RandomActivation
from mesa.batchrunner import BatchRunner

from agent import TreeCell #might have to edit this
#from fake_surface import fake_surface

class demmodel(Model):

    _grid = None
    #change torus boolean to density for visualization in the example
    def __init__(self, x_max, y_max, torus, x_min=0, y_min=0,
                 grid_width=100, grid_height=100):

        self.x_min = x_min
        self.x_max = x_max
        self.torus = torus
        #self.density = density
        self.width = x_max - x_min
        self.y_min = y_min
        self.y_max = y_max
        self.height = y_max - y_min

        self.cell_width = (self.x_max - self.x_min) / grid_width
        self.cell_height = (self.y_max - self.y_min) / grid_height


        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(grid_width, grid_height, torus)

        self.datacollector = DataCollector({"Fine": lambda m: self.count_type(m, "Fine"),"On Fire": lambda m: self.count_type(m, "On Fire"),"Burned Out": lambda m: self.count_type(m, "Burned Out")})


        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if random.random() < torus:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
        self.running = True

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
