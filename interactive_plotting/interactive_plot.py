import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
#import seaborn as sns

plt.rcParams['keymap.zoom'] = '' #disable default zoom key "o"

from optparse import OptionParser
import filterbank
import spectra
import waterfaller_interact as wt

#palette = ListedColormap(sns.diverging_palette(220, 20, n=7).as_hex())


# real FRB from Dominic
filename = '/home/dleduc/hey-aliens/simulateFRBclassification/jiani_FRBs.npy'
frb = np.load(filename)

# datafile from waterfaller
# parameters
start = 16.22
duration = 0.06
dm = 600
nsub = 64
width = 1
sweep_posn = 0.2
cmap = "hot"

rawdatafile = filterbank.FilterbankFile("/mnt_blpd9/datax/incoming/spliced_guppi_57991_49905_DIAG_FRB121102_0011.gpuspec.0001.8.4chan.fil")
data, bins, nbins, start_time = wt.waterfall(rawdatafile, start, duration, dm=dm, nsub=nsub,  width_bins=width)

# data points for plotting
values = data.data
current_values = np.copy(values)

time_signal = np.sum(values, axis=0).flatten()
current_time_signal = time_signal

vmin = np.mean(values)
inc = np.std(values)/10


def average(x, y):
    return (x+y)/2

def avg_timesignal():
    """Reduces bins in time series array"""
    global current_time_signal
    new_row = []

    if (len(current_time_signal) % 2 != 0):
        for i in range(0, len(current_time_signal)-1, 2):
            new_row.append(average(current_time_signal[i], current_time_signal[i+1]))
    else:
        for i in range(0, len(current_time_signal), 2):
            new_row.append(average(current_time_signal[i], current_time_signal[i+1]))
    
    current_time_signal = np.array(new_row)

def avg_cols():
    """Returns array with averaged columns."""
    global current_values
    new_values = []

    for row in current_values:
        new_row = []

        if (len(row) % 2 != 0):
            for i in range(0, len(row)-1, 2):
                new_row.append(average(row[i],row[i+1]))
            new_values.append(new_row)
        else:
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

def replot():
    """Re-plots and updates the current canvas with the new values."""
    global fig, ax, current_values, current_time_signal

    ax[0].cla()
    ax[0].plot(current_time_signal, color='k', scalex=True)
    ax[0].set_xlim(0, len(current_time_signal))

    ax[1].imshow(current_values, vmin=vmin, origin='lower', aspect='auto', cmap=cmap)
    ax[1].set(ylabel = 'Frequency', xlabel='Time')
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
    
    state = -1
    print('you pressed', event.key)

    if event.key == 'o':
        state = 0
    elif event.key =='i':
        state = 1
    elif event.key == 'r':
        state = 2
    elif event.key == 'c':
        state = 3
    elif event.key == '-':
        state = 4
    elif event.key == '+':
        state = 5
    elif event.key == 'q':
        state = -1
        #fig.canvas.mpl_disconnect(fig.canvas.mpl_connect('key_press_event', on_key))
        #fig.canvas.mpl_disconnect(fig.canvas.mpl_connect('button_press_event', onclick))
        sys.exit()
    if state != -1:
        check_state(state) 

def check_state(state):
    """Checks the current state and updates the graph accordingly."""

    global values, current_values, time_signal, current_time_signal, vmin

    if state == 0:
        print('Returning to original plot')
        current_values = np.copy(values)
        current_time_signal = time_signal
        replot()
    elif state == 1:
        print('Reducing resolution')
        avg_rows()
        avg_cols()
        avg_timesignal()
        replot()
    elif state == 2:
        print('Reducing rows')
        avg_rows()
        avg_timesignal()
        replot()
    elif state == 3:
        print('Reducing columns')
        avg_cols()
        replot()
    elif state == 4:
        print('Reducing vmin')
        if vmin - inc < np.min(current_values):
            print('error')
            return
        vmin = vmin - inc
        replot()
    elif state == 5:
        print('Increasing vmin')
        if vmin + inc > np.max(current_values):
            print('error')
            return
        vmin = vmin + inc
        replot()

def onclick(event):
    global current_values

    if event.dblclick:
        print("y-bin is ", event.ydata)
        current_values[int(round(event.ydata))] = np.zeros(np.shape(current_values)[1])
        replot()

def main():
    global fig, ax

    wt.plot_waterfall(data, start, duration, dm, "unknown_cand", cmap_str=cmap, sweep_posns=sweep_posn)

    fig, ax  = plt.subplots(2, gridspec_kw={'height_ratios':[1,3]})

    ax[0].plot(time_signal, color='k', scalex=True)
    ax[0].set_xlim(0, len(current_time_signal))
    #ax[0].axes.get_yaxis().set_ticks([])
    #ax[0].axes.get_xaxis().set_ticks([])

    ax[1].imshow(current_values, vmin=vmin, origin='lower', aspect='auto', cmap=cmap)
    ax[1].set(ylabel = 'Frequency', xlabel='Time')

    fig.canvas.mpl_connect('key_press_event', on_key)
    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

main()
