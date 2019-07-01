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
        passengers_in_need = False
        while(True):
            for train in self.trains_in_station:
                assert (train.in_station == True)
                # let passengers on train leave first
                for p in train.passengers:
                    if p.destination == self.station_type:
                        train.passengers.remove(p)

                if (len(train.passengers) >= train.capacity):
                    # move full trains out of station
                    train.in_station = False
                    self.trains_in_station.remove(train)
                else:
                    for p in self.passengers:
                        if (any([p.destination == s.station_type for s in train.next_stations])):
                            passengers_in_need = True
                            train.passengers.append(p)
                            self.passengers.remove(p)

            if (passengers_in_need == False):
                break
            