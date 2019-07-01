from Line import Line
from Station import Station
from Train import Train
import numpy as np
from PIL import Image, ImageDraw
from utils import totuple, get_rect, draw_ellipse, angle

class Game:
    def __init__(self, window_size):
        self.window_size = 1000
        self.margin = 50
        self.ticks = 0
        normal_speed = 0.05 * self.window_size
        self.trains = [
            Train("train 1", normal_speed, 0, 1)
            # Train("train 1", normal_speed, 0, 1), 
            # Train("train 2", normal_speed, 0, 1), 
            # Train("train 3", normal_speed, 0, 1), 
        ]
        self.stations = [
            Station("station 1", "triangle", self.spawn_xy()), 
            Station("station 2", "square", self.spawn_xy()),
            Station("station 3", "circle", self.spawn_xy())
        ]

        self.lines = []
        self.available_special_types = ["diamond"]
        self.carriage_num = 0
        self.score = 0
        self.day = 0

    def spawn_xy(self):
        x = np.random.randint(self.margin, self.window_size-self.margin)
        y = np.random.randint(self.margin, self.window_size-self.margin)
        return np.array([x, y], dtype=np.float)
    
    def step(self):
        self.ticks += 1
        if self.ticks % 299 == 0:
            self.day += 1
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
                    station_type = np.random.choice(self.available_special_types)
            new_station = Station("station "+str(self.day+3), station_type, self.spawn_xy())
            self.stations.append(new_station)

        if self.ticks % 29 == 0:
            # populate stations
            for station in self.stations:
                if np.random.random() < 0.5:
                    station.populate(self.available_special_types)
        
        for line in self.lines:
            for train in line.trains:
                if train.in_station:
                    train.station.move_passengers()
                else:
                    train.move()
        
    def draw(self):
        # draw background
        side = self.window_size
        line_width = int(0.01 * side)
        square_size = int(0.025 * side)
        triangle_size = int(0.05 * side)
        train_width = int(0.02 * side)
        train_height = int(0.06 * side)
        img = Image.new(mode='RGB', size=(side, side), color=(255, 255, 255))
        draw_img = ImageDraw.Draw(img)

        # draw lines
        for l in self.lines:
            line = []
            for s in l.stations:
                line.append(totuple(s.xy))
            draw_img.line(line, fill=(0, 0, 0), width=line_width)
        
        # draw stations
        for s in self.stations:
            if s.station_type == "circle":
                radius = 0.025 * side
                x0, y0 = s.xy
                x1 = x0 + radius
                y1 = y0 + radius
                # draw image
                draw_ellipse(draw=draw_img, bbox=[x0, y0, x1, y1], linewidth=line_width)
            else:
                if s.station_type == "triangle":
                    L = triangle_size
                    corners = np.array([[0, 0],
                            [L, 0], 
                            [0.5 * L, 0.866 * L],
                            [0, 0]])
                    corners += s.xy
                elif s.station_type == "square":
                    corners = get_rect(s.xy[0], s.xy[1], square_size, square_size, 0)
                elif s.station_type == "diamond": 
                    corners = get_rect(s.xy[0], s.xy[1], square_size, square_size, 90)

            # get tuple version of the points
            shape_tuple = totuple(corners)
            # draw image
            draw_img.polygon(xy=[tuple(p) for p in corners], fill=(255, 255, 255), outline=0)
            # draw line around polygon to adjust line width since polygon doesn't support it
            draw_img.line(xy=shape_tuple, fill=(0, 0, 0), width=line_width)
        
        # draw trains
        for t in self.trains:
            corners = get_rect(t.xy[0], t.xy[1], train_height, train_width, t.angle)
            # get tuple version of the points
            shape_tuple = totuple(corners)
            # draw image
            draw_img.polygon(xy=[tuple(p) for p in corners], fill=(0, 0, 0), outline=0)
        
        image = np.asarray(img)
        image = np.copy(image)
        image = image / 255.0

        return image