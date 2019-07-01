import numpy as np
import copy

def deepcopy(x):
    return copy.deepcopy(x)

def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def magnitude(v):
    return np.sqrt(v[0]**2 + v[1]**2)

def unit_vector(v):
    """ 
    Returns the unit vector of the vector.  
    """

    return v / np.linalg.norm(v)

def angle(v1, v2):
    """ 
    Returns the angle in radians between vectors 'v1' and 'v2'::

    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_rect(x, y, width, height, angle):
    """
    Utility function to create rectangles using PIL.ImageDraw
    """

    rect = np.array([(0, 0), (width, 0), (width, height), (0, height), (0, 0)])
    theta = (np.pi / 180.0) * angle
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    offset = np.array([x, y])
    transformed_rect = np.dot(rect, R) + offset
    return transformed_rect

def totuple(a):
    """
    Convert a numpy array to a tuple of tuples in the format of ((), ())
    """
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

def draw_ellipse(draw, bbox, linewidth):
    """
    Draw two concentric ellipses to create an ellipse with arbitrary line width. 
    PIL.ImageDraw does not natively support linewidth as an input, thus the workaround. 

    Inputs:
    =======
    draw: ImageDraw.Draw instance
    bbox: list or np.array in the format of [x0, y0, x1, y1]. This bbox enclose the ellipse. 
    linewidth: int

    Outputs:
    ========
    draw: ImageDraw.Draw instance -- the updated version of the input `draw`. 
    """
    for offset, fill in (linewidth/-2.0, 'black'), (linewidth/2.0, 'white'):
        left, top = [(value + offset) for value in bbox[:2]]
        right, bottom = [(value - offset) for value in bbox[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)
        
    return draw