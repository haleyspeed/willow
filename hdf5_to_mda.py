"""Python script to convert Leaf Labs HDF5 output to MountainSort MDA file
Queries primary data for
1. sample_index
2. aux_data
3. channel_data (contains the actual data we need to xfer)
4. chip_live
"""
import h5py
import numpy as np
import os
from mlpy import mdaio
import matplotlib.pyplot as plt

# File Functions
fin = '20200324-third.h5'
f = h5py.File(fin, 'r')
sample_rate = 30000
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

# 16-bit save function
# mdaio.mdaio.writemda16i(out,'raw16.mda')

# 32bit save function
mdaio.writemda32(out,'raw.mda')

# (Optional) Plot the first 20000 datapoints from channel 500
channel = 0 # chip number/sample_id
x_start = 0
x_end = 3000

fig, ax = plt.subplots(figsize=(8, 8), frameon = False, dpi = 100)
x = list(range(rows-1))
y = (out[0:(rows-1), channel]) * 0.195 # scaled to microvolts
ax.plot(x, y, lw = 1)
ax.set_xlabel ("unscaled datapoints")
ax.set_ylabel("microvolts")
ax.set_xlim(x_start,x_end)
plt.show()

f.close()
