import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage, interpolate
import sys

np.random.seed(42)
n = 256
p = 0.5 #order of scipy.ndimage spline zoom
values = np.random.random_sample((n,n))

def interp(n, values):
    return interpolate.RectBivariateSpline(np.linspace(0,1,n), np.linspace(0,1,n), values)

def zoom(values, p):
    return ndimage.zoom(values, p)

def on_key(event):
    plt.clf()
    plt.imshow(zoom(values, p))

    print('you pressed', event.key)

    f = interp(n, values)

    if event.key == 'i':
        fig.clf()
        plt.imshow(zoom(values, p))
    elif event.key == 'r':
        fig.clf()
        plt.imshow(f(np.linspace(0,1,int(n/2)),np.linspace(0,1,n)))
    elif event.key == 'c':
        fig.clf()
        plt.imshow(f(np.linspace(0,1,n),np.linspace(0,1,int(n/2))))
    elif event.key == 'q':
        fig.canvas.mpl_disconnect(cid)


fig = plt.figure()
plt.imshow(values)
cid = fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()
