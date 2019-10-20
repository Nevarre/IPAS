import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage, interpolate
import sys

np.random.seed(42)
n = 256
p = 0.5 #order of scipy.ndimage spline zoom
values = np.random.random_sample((n,n))


state = 0

def interp(n, values):
    return interpolate.RectBivariateSpline(np.linspace(0,1,n), np.linspace(0,1,n), values)

def zoom(values, p):
    return ndimage.zoom(values, p)

def on_key(event):
    print('you pressed', event.key)

    if event.key == 'i':
        state = 1
    elif event.key == 'r':
        state = 2
    elif event.key == 'c':
        state = 3
    elif event.key =='u':
        state = 0
    elif event.key == 'q':
        fig.canvas.mpl_disconnect(cid)
        state = -1
    check_state(state) 

def check_state(stat):
    f = interp(n, values)

    if stat == 0:
        print('Returning to original plot')
        plt.imshow(values)
        fig.canvas.draw()
    elif stat == 1:
        print('Reducing resolution to 128x128')
        plt.imshow(zoom(values, p))
        fig.canvas.draw()
    elif stat == 2:
        print('Reducing resolution to 128x256')
        plt.imshow(f(np.linspace(0,1,int(n/2)),np.linspace(0,1,n)))
        fig.canvas.draw()
    elif stat == 3:
        print('Reducing resolution to 256x128')
        plt.imshow(f(np.linspace(0,1,n),np.linspace(0,1,int(n/2))))
        fig.canvas.draw()


fig = plt.figure()
plt.imshow(values)
cid = fig.canvas.mpl_connect('key_press_event', on_key)
 
plt.show()
