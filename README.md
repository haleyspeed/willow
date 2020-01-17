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
* Had to manually create a package called "mlpy" in the Anaconda3\envs\h5test\Lib\site-packages using the files (mdaio.py) in https://github.com/flatironinstitute/mountainsort/tree/master/packages/pyms/mlpy for the hdf5_to_mda.py script

### Running Mountainsort
* Runs best on linux. Can run on Mac. Use conda environments to avoid installation errors
* See https://users.flatironinstitute.org/~magland/docs/mountainsort
* And https://github.com/flatironinstitute/mountainsort_examples/blob/master/README.md
* Conda installation instructions did not work for me as written, but this did:
	* conda install -c flatiron mountainlab 
	* conda install -c flatiron mountainlabmountainlab_pytools 
	* conda install -c flatiron mountainlabml_ephys 
	* conda install -c flatiron mountainlabml_ms3 
	* conda install -c flatiron mountainlabml_ms4alg 
	* conda install -c flatiron mountainlabml_pyms

