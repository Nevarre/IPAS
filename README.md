## Interactive Plotting
Breakthrough Listen interactive plotter for astronomical radio sources.

## OVERVIEW
An interactive plotting tool supporting .fil files from the Breakthrough Listen Open Data Archive. Interactive functions support adjusting signal to noise ratio by downsampling and subbanning frequency channels, adjusting contrast of colormap, and flagging unwanted channels.

The Breakthrough Listen initiative aims to search for extraterrestrial life by looking for alien technosignatures. These technosignatures are often masked by radio frequency interference (RFI) such as Wi-Fi, cellphone signals, or any unwanted signals from Earth. We suspect technosignatures to come in the form of transient signals, in particular, Fast Radio Bursts (FRB). Part of this project is using machine learning tools to classify FRB signals. However candidates classified with machine learning are not necessarily a real FRB signals. The main purpose of this GUI is to provide an efficient method for human users to search through these potential FRB candidates and confirm the authenticity of the candidates discovered by machine learning techniques.

### BUILD REQUIREMENTS

* [NumPy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/3.1.1/users/installing.html)
* [SciPy](https://www.scipy.org/install.html)
* [Presto](https://github.com/scottransom/presto)
* [pypulsar](https://github.com/plazar/pypulsar)

### USAGE


| Key command    | Function     |
| ------------- |:-------------:|
| `o`    | reverts to original state |
| `i`    | reduces columns and rows together |
| `r`    | reduces rows (subbanning) |
| `c`    |  reduces columns (downsampling) |
| `-`    | reduces contrast |
| `+`    | increases contrast |
| `shift` + `D` + `_`   | decreases dispersion |
| `shift` + `D` + `+`   | increases dispersion |
| `q`    | quits GUI |

### Example

The figure below shows how a real FRB signal (figure 1) and altered signal (figure 2). The dispersion has been reduced by 20 and subbanded 3 times.

![alt text][figure 1]
![alt text][figure 2]

[figure 1]: https://github.com/stevecroft/bl-interns/blob/master/jianic/example_signals/A_unknown_cand_16.220_600.png
[figure 2]: https://github.com/stevecroft/bl-interns/blob/master/jianic/example_signals/unknown_cand_16.220_580.png


#### Future Work

* Flagging channels still has to be fixed to interact with waterfaller.py
* Customizable colormaps or option to cycle through colormap
* Option parser for quicker access to GUI
