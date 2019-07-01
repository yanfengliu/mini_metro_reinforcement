from utils import dist, magnitude, unit_vector, angle, deepcopy
import numpy as np

class Train:
    def __init__(self, name, speed, idx, direction):
        self.name = name
        self.line = None
        self.speed = speed
        self.velocity_unit_v = np.array([0, 0])
        self.xy = []
        self.station = None
        self.idx = idx
        self.in_station = False
        self.passengers = []
        self.next_stations = []
        self.direction = direction
        self.capacity = 6
        self.angle = 0

    def attach_to_line(self, line, idx):
        self.line_stations = line.stations
        line.trains.append(self)
        self.next_stations = line.stations[1:]
        self.station = line.stations[idx]
        self.direction = 1
        self.xy = deepcopy(line.stations[idx].xy)
        next_station = self.next_stations[0]
        offset = next_station.xy - self.xy
        self.angle = np.arctan2(-offset[1], offset[0])*(180/np.pi)
        self.velocity_unit_v = unit_vector(offset)
    
    def move(self):
        next_station = self.next_stations[0]
        # check if final stop
        if (len(self.next_stations) == 1):
            next_stations = self.line_stations[::-self.direction]
            self.direction = -self.direction
            station_after_next = next_stations[0]
        else:
            station_after_next = self.next_stations[1]

        # update location and velocity
        if (dist(next_station.xy, self.xy) >= self.speed):
            self.xy += self.speed * self.velocity_unit_v
        else:
            dist_travelled = dist(next_station.xy, self.xy)
            offset = station_after_next.xy - next_station.xy
            self.angle = np.arctan2(-offset[1], offset[0])*(180/np.pi)
            self.velocity_unit_v = unit_vector(offset)
            # TODO: check if need to stop
            # stop if passengers on train need to leave or passengers on station need to board
            if ((next_station.station_type in [x.destination for x in self.passengers]) or 
                (any([x.destination == y.station_type for x, y in zip(next_station.passengers, self.next_stations)]))):
                self.xy = self.xy = deepcopy(next_station.xy)
                self.station = next_station
                next_station.trains_in_station.append(self)
                self.in_station = True
                self.next_stations.remove(next_station)
            else:
                self.xy = next_station.xy + (self.speed - dist_travelled) * self.velocity_unit_v
        
            # update next stations
            self.station = next_station
            del self.next_stations[0]
            if (len(self.next_stations) == 0):
                self.next_stations = self.line_stations[::-self.direction]