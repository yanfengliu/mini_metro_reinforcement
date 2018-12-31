from Line import Line
from Station import Station
from Train import Train
import numpy as np

class Game:
    def __init__(self, width, height):
        self.margin = 50
        self.ticks = 0
        self.width = width
        self.height = height
        normal_speed = 0.01 * self.width
        self.trains = [
            Train("train 1", normal_speed), 
            Train("train 2", normal_speed), 
            Train("train 3", normal_speed), 
        ]
        self.stations = [
            Station("station 1", "triangle", self.spawn_xy()), 
            Station("station 2", "square", self.spawn_xy()),
            Station("station 3", "circle", self.spawn_xy())
        ]
        self.lines = []
        self.available_special_types = []
        self.carriage_num = 0
        self.score = 0
        self.day = 0

    def spawn_xy(self):
        x = np.random.randint(self.margin, self.width-self.margin)
        y = np.random.randint(self.margin, self.height-self.margin)
        return [x, y]
    
    def step(self):
        self.ticks += 1
        if self.ticks % 299 == 0:
            self.day += 1

        # populate stations
        for station in self.stations:
            station.populate(self.available_special_types)
        
        for line in self.lines:
            for train in line.trains:
                if train.in_station:
                    train.station.move_passengers()
                else:
                    train.move()
        