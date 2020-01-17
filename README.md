# Willow Hacks
Collection of python scripts to export and analyze HDF5 files from the Leaf Labs Willow Ultra-High-Density recording system. The repository currently focuses on using Mountainsort to do spike sorting on 1024-channel datasets.

### Contains:
* hdf5_to_mda.py  
  * Converts HDF5 files to the mda format for use with mountainsort
* verify_nmda.py  
  * Verifies faithful conversion of hdf5 data to mda format
* probe_map.py    
  * Makes probe maps for the geom.csv requirement for mountainsort

### Notes
* These are bare-bones scripts written to make willow's output compatible with Mountainsort
* There is no conversion of units, just raw data, so it is up to the user to know: 
  * The sample rate for the .json file (30000 Hz = default for leaf)
  * Scale factor for conversion of raw data to microvolts (0.195 according to Leaf Labs hdf52dat.m script)
* Probe geometry will vary between manufacturers and the number of probes/shanks/channels used
  * May need multiple probe geometries depending on the experimental setup

### Running Mountainsort
See users.flatironinstitute.org/~magland/docs/mountainsort
And https://github.com/flatironinstitute/mountainsort_examples/blob/master/README.md
