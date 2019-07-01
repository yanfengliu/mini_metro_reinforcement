import Game
import Line
import Train
import Station
import utils

import matplotlib.pyplot as plt
import numpy as np

g = Game.Game(1000)
l = Line.Line("line 1", g.stations)
g.trains[0].attach_to_line(l, 0)
g.lines.append(l)
plt.figure(figsize=(8, 8))
while True:
    g.step()
    I = g.draw()
    plt.imshow(I)