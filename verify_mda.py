import numpy as np
from mlpy import mdaio
import matplotlib.pyplot as plt
import os

# Load in the mda file
din = r'C:\Users\haley\Dropbox\Projects\LeafLabs\ms_test'
os.chdir(din)
d = mdaio.readmda('newfile_16bit_integer.mda')

# get attributes of the dataset
dshape = d.shape
rows = dshape[0]
columns = dshape[1]
print ('rows: ' + str(rows))
print ('columns: ' + str(columns))
print ('size: ' + str(d.size))

# Plot the first 20000 datapoints from channel 500
channel = 500 # chip number/sample_id
x_start = -100
x_end = 20000

fig, ax = plt.subplots(figsize=(8, 8), frameon = False, dpi = 100)
x = list(range(rows-1))
y = (d[0:(rows-1), channel]) * 0.195 # scaled to microvolts 
ax.plot(x, y, lw = 1)
ax.set_xlabel ("unscaled datapoints")
ax.set_ylabel("microvolts")
ax.set_xlim(x_start,x_end)
plt.show()


