from utils import dist, magnitude, unit_vector, angle
import numpy as np

class Train:
    def __init__(self, name, speed):
        self.name = name
        self.line = None
        self.speed = speed
        self.velocity_unit_v = np.array([0, 0])
        self.carriage = []
        self.xy = []
        self.station = None
        self.idx = 0
        self.in_station = 0
        self.passengers = []
    
    def move(self):
        next_station = self.line.stations[self.idx+1]
        if (dist(next_station.xy, self.xy) <= magnitude(self.speed)):
            self.xy += self.speed * self.velocity_unit_v
        else:
            dist_travelled = dist(next_station.xy, self.xy)
            station_after_next = self.line.stations[self.idx+2]
            speed_angle = angle(next_station.xy, station_after_next.xy)
            self.velocity_unit_v = np.array([np.cos(speed_angle), np.sin(speed_angle)])
            # TODO: check if need to stop

            self.xy = next_station.xy + (self.speed - dist_travelled) * self.velocity_unit_v        