## Interactive Plotting
Breakthrough Listen interactive plotter for astronomical radio sources.

## OVERVIEW
An interactive plotting tool supporting .fil files from the Breakthrough Listen Open Data Archive. Interactive functions support adjusting signal to noise ratio by downsampling and subbanning frequency channels, adjusting contrast of colormap, and flagging unwanted channels.

The Breakthrough Listen initiative aims to search for extraterrestrial life by looking for alien technosignatures. These technosignatures are often masked by radio frequency interference (RFI) such as Wi-Fi, cellphone signals, or any unwanted signals from Earth. We suspect technosignatures to come in the form of transient signals, in particular, Fast Radio Bursts (FRB). Part of this project is using machine learning tools to classify FRB signals. However candidates classified with machine learning are not necessarily a real FRB signals. The main purpose of this GUI is to provide an efficient method for human users to search through these potential FRB candidates and confirm the authenticity of the candidates discovered by machine learning techniques.

### BUILD REQUIREMENTS

numpy
matplotlib
filterbank
spectra
scipy
pdat pulsar data toolbox

### USAGE

Key shortcuts:

o - reverts to original state
i - reduces columns and rows together
r - reduces rows (subbanning)
c - reduces columns (downsampling)
- - reduces contrast
+ - increases contrast
shift + D + _ - decreases dispersion
shift + D + + - increases dispersion
q - quits GUI

