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

# Plot the first 500 datapoints from ch0
fig, ax = plt.subplots(figsize=(3, 4), frameon = False, dpi = 100)
x = list(range(rows-1))
ax.plot(x, d[0:(rows-1),0])
plt.show()

