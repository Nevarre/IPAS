import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage, interpolate

np.random.seed(42)

n = 256
p = 0.5 #order of scipy.ndimage spline zoom
values = np.random.random_sample((n,n))


state = 0

def interp(n, values):
    """Returns interpolation function used for reducing either the rows or columns of matrix. """
    return interpolate.RectBivariateSpline(np.linspace(0,1,n), np.linspace(0,1,n), values)

def zoom(values, p):
    """Returns new array that has been interpolated by order of p."""
    return ndimage.zoom(values, p)

def replot(values):
    """Re-plots and updates the current canvas with the new values."""
    plt.imshow(values, origin='lower')
    fig.canvas.draw()

def on_key(event):
    """
    Assigns the new state determined by key-press event from user.
    Key-presses:
        "o" - Return to original state.
        "i" - Zoom in onto plot by reducing the resolution by half.
        "r" - Reduce the bins along the rows of the array.
        "c" - Reduce the bins along the columns of the array.
        "q" - Quit and exit plotting tool.
    
    """
    print('you pressed', event.key)

    if event.key == 'o':
        state = 0
    elif event.key =='i':
        state = 1
    elif event.key == 'r':
        state = 2
    elif event.key == 'c':
        state = 3
    elif event.key == 'q':
        state = -1
        fig.canvas.mpl_disconnect(cid)

    if state != -1:
        check_state(state) 

def check_state(state):
    """Checks the current state and updates the graph accordingly."""
    f = interp(n, values)

    if state == 0:
        print('Returning to original plot')
        replot(values)
    elif state == 1:
        print('Reducing resolution to 128x128')
        replot(zoom(values, p))
    elif state == 2:
        print('Reducing resolution to 128x256')
        replot(f(np.linspace(0,1,int(n/2)),np.linspace(0,1,n)))
    elif state == 3:
        print('Reducing resolution to 256x128')
        replot(f(np.linspace(0,1,n),np.linspace(0,1,int(n/2))))


fig = plt.figure()
plt.imshow(values, origin='lower')
cid = fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()
