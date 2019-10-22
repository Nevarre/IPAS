import numpy as np
from matplotlib import pyplot as plt

np.random.seed(42)

n = 256
values = np.random.random_sample((n,n))
current_values = values

def average(x, y):
    return (x+y)/2

def avg_cols():
    """Returns array with averaged columns."""
    global current_values
    new_values = []

    for row in current_values:
        new_row = []
        for i in range(0, len(row), 2):
            new_row.append(average(row[i],row[i+1]))
        new_values.append(new_row)
    current_values = new_values

def avg_rows():
    """Returns array with averaged rows."""
    global current_values
    current_values = np.transpose(current_values)
    avg_cols()
    current_values = np.transpose(current_values)

def replot(val):
    """Re-plots and updates the current canvas with the new values."""
    plt.imshow(val, origin='lower', aspect='auto')
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

    global current_values

    if state == 0:
        print('Returning to original plot')
        current_values = values
        replot(values)
    elif state == 1:
        print('Reducing resolution to 128x128')
        avg_rows()
        avg_cols()
        replot(current_values)
    elif state == 2:
        print('Reducing resolution to 128x256')
        avg_rows()
        replot(current_values)
    elif state == 3:
        print('Reducing resolution to 256x128')
        avg_cols()
        replot(current_values)


fig = plt.figure()
plt.imshow(values, origin='lower', aspect='auto')
cid = fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()
