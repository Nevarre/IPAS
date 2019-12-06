import sys
import numpy as np
from matplotlib import pyplot as plt
#from matplotlib.colors import ListedColormap
#import seaborn as sns
#palette = ListedColormap(sns.diverging_palette(220, 20, n=7).as_hex())

plt.rcParams['keymap.zoom'] = '' #disable default zoom key "o"

from optparse import OptionParser
import filterbank
import spectra
import waterfaller_interact_v2_working as wt
import copy

# datafile from waterfaller
# parameters
start = 16.22
duration = 0.06
dm = 600
nsub = 3712
width = 1
sweep_posn = 0.2
cmap = "hot"

rawdatafile = filterbank.FilterbankFile("/mnt_blpd9/datax/incoming/spliced_guppi_57991_49905_DIAG_FRB121102_0011.gpuspec.0001.8.4chan.fil")
data, bins, nbins, start_time, source_name = wt.waterfall(rawdatafile, start, duration, dm=dm, nsub=nsub,  width_bins=width)

# global values
static_data = copy.deepcopy(data)
current_data = copy.deepcopy(data)

values = np.copy(data.data)
current_values = np.copy(data.data)

downsamp = 1
numchan = data.numchans
vmin = 0
#vmin = np.mean(values)
inc = np.std(values)/10

static_dm = dm

keys2 = ['','']
cntr = 0


def avg_cols():
    """Returns array with downsampled columns by 2. """
    global current_values, downsamp, current_data

    downsamp += 2
    current_data.downsample(downsamp)
    current_values = np.copy(current_data.data)
    
def avg_rows():
    """Returns array with subbanded rows by half."""
    global current_values, current_data, numchan

    numchan = numchan/2
    current_data.subband(numchan) 
    current_values = np.copy(current_data.data)

def replot():
    """Re-plots and updates the current canvas with the new values."""
    global fig

    plt.clf()
    wt.plot_waterfall(current_data, start, fig, "unknown", duration, dm, "unknown_cand", cmap_str=cmap,width=1,snr=10) #Old plot
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
    global keys2, cntr

    state = -1
    print('you pressed', event.key)
    
    if( event.key == 'shift'):
        cntr = 1;
    elif (cntr == 1):
        keys2[0] = event.key
        cntr = 2
    elif cntr == 2:
        keys2[1] = event.key
    else:
        cntr = 0

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
    elif cntr == 2 and keys2[0]+keys2[1] == 'D_':
        cntr == 0
        state = 6
    elif cntr == 2 and keys2[0]+keys2[1] == 'D+':
        cntr == 0
        state = 7
    elif event.key == 'q':
        state = -1
        sys.exit()
    if state != -1:
        check_state(state) 

def check_state(state):
    """Checks the current state and updates the graph accordingly."""

    global current_values, current_data, vmin, downsamp, numchan, dm

    if state == 0:
        print('Returning to original plot')
        current_data = copy.deepcopy(static_data)
        current_values = np.copy(current_data.data)
        downsamp = 0
        numchan = static_data.numchans
        dm = static_dm
        replot()
    elif state == 1:
        print('Reducing resolution')
        avg_rows()
        avg_cols()
        replot()
    elif state == 2:
        print('Reducing rows')
        avg_rows()
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
    elif state == 6:
        print('Decreasing dispersion')
        dm -= 5
        replot()
    elif state == 7:
        print('Increasing dispersion')
        dm += 5
        replot()

def onclick(event):
    global current_values

    if event.dblclick:
        print("y-bin is ", event.ydata)
        current_values[int(round(event.ydata))] = np.zeros(np.shape(current_values)[1])
        replot()

def main():
    global fig, ax

    fig = plt.figure(figsize=(6,8)) 

    wt.plot_waterfall(data, start, fig, "unknown", duration, dm, "unknown_cand", cmap_str=cmap,width=1,snr=10) #Old plot
    	
    fig.canvas.mpl_connect('key_press_event', on_key)
    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

main()
