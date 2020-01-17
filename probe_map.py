import os
import numpy as np

# User Input
shank_channels = 32
shank_rows = 16
shank_columns = 2
max_channels = 1024
dout = r'C:\Users\haley\Dropbox\Projects\LeafLabs\ms_test'

# Create the probe map
out = []
channel = 0
for channel in range(0, max_channels):
    shank = int(channel // shank_channels)
    probe_site = channel - (shank * shank_channels)
    col = int(probe_site // shank_rows)
    row = probe_site - (col * shank_rows)
    app = [channel, shank, row, col]
    out.append(app)
    #print (app)

arr = np.array(out)
np.savetxt('geom.csv', arr, fmt = '%s', delimiter = ',')

    

