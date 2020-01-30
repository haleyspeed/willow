# Python script to convert Leaf Labs HDF5 output to MountainSort MDA file
# Queries primary data for 
# 1. sample_index 
# 2. aux_data
# 3. channel_data (contains the actual data we need to xfer)
# 4. chip_live

import h5py
import numpy as np
import os
from mlpy import mdaio
import matplotlib.pyplot as plt


# File Functions
fin = '2020_01_08.h5'
din = r'C:\Users\haley\Dropbox\Projects\LeafLabs\ms_test'
dout = din
os.chdir (din)
f = h5py.File(fin, 'r')
# print(f.keys())


# Assign keys to variables
si = f.get('sample_index')
aux = f.get('aux_data')
ch = f.get('channel_data')
chip = f.get('chip_data')

# Make an N X M array with M = number of channels and N = # timepoints
out = np.array(ch)
rows = out.shape[0]
cols = out.shape[1]

# Use 32bit save function or you will get misshapen waveforms (like saturated gain)
mdaio.writemda32(out,'newfile_16bit_integer.mda')

# Plot the first 500 datapoints from ch0
fig, ax = plt.subplots(figsize=(3, 4), frameon = False, dpi = 100)
x = list(range(rows-1))
ax.plot(x, out[0:(rows-1),0])
plt.show()

f.close()
