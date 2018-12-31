import numpy as np
from Passenger import *

class Station:
    def __init__(self, name, station_type, xy):
        self.population = 0
        self.name = name
        self.station_type = station_type
        self.xy = xy
        self.passengers = []
        self.trains_in_station = []
    
    def populate(self, available_special_types):
        t1 = np.random.random()
        if t1 < 0.3:
            t2 = np.random.random()
            if t2 < 0.3:
                station_type = "triangle"
            elif t2 < 0.6:
                station_type = "square"
            elif t2 < 0.9:
                station_type = "circle"
            else:
                station_type = np.random.choice(available_special_types)
            self.passengers.append(Passenger(station_type))
    
    def move_passengers(self):
        for train in self.trains_in_station:
            assert (train.in_station == 1)
            