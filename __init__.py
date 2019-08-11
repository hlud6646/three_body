import numpy as np
from itertools import product


def init_state():
    state = np.empty(3, dtype=[('location', float, 2),
                               ('velocity', float, 2),
                               ('mass',      float, 1),
                               ('color',     float, 3)])
    state['location'] = np.random.uniform(.25, .75, (3, 2))
    state['velocity'] = np.zeros((3, 2))
    state['mass'] = np.ones(3)
    state['color'] = np.random.uniform(.2, .9, (3, 3))
    # shift location so that center of mass is origin.
    return state


def force(a, b):
    """ Return the gravitational force that b exerts on a. """
    G = 10e-5
    v = b['location'] - a['location']
    d = sum(v*v)**.5
    return (G*a['mass']*b['mass']/d**2)*v


def update(state):
    DT = 10e-3
    a, b, c = state
    q, w, e = [force(a, b), force(a, c), force(b, c)]
    net_force = np.array([q+w, e-q, -e-w])
    state['velocity'] += DT*net_force
    state['location'] += DT*state['velocity']


def make_disk():
    """ make a round mask for drawing the point masses. """
    r = 4
    disk = np.ones((2*r, 2*r, 3))
    for y, x in product(range(2*r), repeat=2):
        d2 = (x-r)**2 + (y-r)**2
        disk[y][x] = int(d2 < r*r) * (1 - d2/(r**2))
    return disk[1:, 1:]


def plot(state, canvas, color_factor):
    """ color_factor should by 1 if cv2 is used to write jpegs. """
    height, width = canvas.shape[:2]
    disk = make_disk()
    for mass in state:
        # the unit square is stretched to fit the canvas,
        # so if any mass is too close to the edge then don't try to draw it.
        if .1 > np.max(np.abs(mass['location'])) > .9:
            continue
        x, y = mass['location']
        x = int(x*width)
        y = int(y*height)
        r = 3
        try:  # should not need this try clause.
            canvas[y:y+2*r+1, x:x+2*r+1] += disk*(mass['color']*3)*color_factor
        except ValueError as e:
            print(e)
            pass


def gen(height, width, color_factor=1):
    state = init_state()
    canvas = np.zeros((height, width, 3), np.float32)
    while True:
        for i in range(30):
            canvas *= 0.999
            update(state)
            plot(state, canvas, color_factor)
        yield canvas


if __name__ == "__main__":

    height, width = 360, 720
    import cv2
    w = cv2.namedWindow("win")
    for frame in gen(height, width, 0.005):
        cv2.imshow('win', frame)
        if cv2.waitKey(int(1000/60)) != -1:
            break
    cv2.destroyAllWindows()
