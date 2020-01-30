# Spike Sorting with Willow Leaf System and Mountainsort 
Collection of python scripts to export and analyze HDF5 files from the Leaf Labs Willow Ultra-High-Density recording system into the Mountainsort data format (.mda). for spike sorting on 1024-channel datasets. Contains additional scripts and tweaked packages to make Mountainsort4 work with Willow output.

### Contains:
_**hdf5_to_mda.py**_ --> Converts HDF5 files to the mda format for use with mountainsort

_**verify_nmda.py**_  -->  Verifies faithful conversion of hdf5 data to mda format

_**probe_map.py**_ --> Makes probe maps for the geom.csv requirement for mountainsort

_**geom.csv**_ --> Sample probe map made by probe_map.py

_**params.json**_ --> Contains configuration information for Mountainsort (sample rate, spike flag)

_**mountainsort.py**_ --> The main file to configure and run Mountainsort4

_**mountainlab4.py**_ --> Edited from original mountainsort package. Replace the file in `site_packages/spikesorters/mountainsort4/`

_**basesorter.py**_ --> Edited from original mountainsort package. Replace the file in ` /site_packages/spikesorters/`


Sample data for testing can be found at n-coding.net

_**Willow Data File**_ --> https://n-coding.net/test_files/willow/mountainsort/2020_01_08.h5

_**Mountainsort Data File**_ --> https://n-coding.net/test_files/willow/mountainsort/raw.mda

*Note: The test data were obtained with a dummy probe and do not contain spikes. That means Mountainsort returns an empty dataset and triggers the error "Mountainsort4Sorter has no attribute 'get_unit_ids". Test files with spikes will be updated once our new probe design has been fabricated (expected Feb/March 2020).

### Changes to Mountainsort4 packages
Mountainsort4 is still under development, especially as it relates to the spikeinterface framework. Packages have moved since the documentation was last updated and many variables within individual packages are set to testing paramaters. Also many functions that once took kwargs now take an instance of a class (i.e. BaseSorter). This raises many errors. I have corrected the following so that Mountainsort4 runs smoothly:
 * Manually create a package called "mlpy" in the Anaconda3\envs\h5test\Lib\site-packages using the files (mdaio.py) in https://github.com/flatironinstitute/mountainsort/tree/master/packages/pyms/mlpy for the hdf5_to_mda.py script
* In the BaseSorter class, the default parameters were set to raise flags in testing:
  * sorter_name is blank but later a function calls to see if it is installed, which raises a flag. Also, the "installed" variable is also set to "False" as default, which automatically halts the script. I changed this to True and ignore the sorter_name altogether because we manually specify the sorter in our script.
  * To initialize an instance of the basesorter class: basesorter = ss.BaseSorter(recording = recording, output_folder = din)
  * If you want to change the default parameters of the basesorter, like the spike detect sign from -1 to 0, then access it as: basesorter.detect_sign = 0. In real life, if you do this, make sure the change in detect sign is also reflected in your params.json file.
* in mountainlab4.py file, the __init__.py was not set to accept the new basesorter class, but rather the old kwargs. However, the __init__ function still calls an instance of the basesorter class. to overcome this, I changed the "__ init__(self, ** kwargs):" to "__ init__(self, BaseSorter, ** kwargs):" 
* Error: 'MdaSortingExtractor' has no attribute "writeSorting" --> error was traced back to the spikeextractor package 
  * Added an import statement to correct this in _**mountainsort.py**_
  
  ~~~
  import spikeextractors as sx
  sx.MdaSortingExtractor.writeSorting(sorting = sorting, save_path = "firings.mda"
  ~~~
  
 * Error: "Mountiansort4Sorter has no attribute "get_unit_ids" --> This happens when there are no spikes detected.
 
Detailed explanations of each of the errors I encountered and how I corrected them can be found in the blog post on n-coding.net (in progress) 


### Notes
* These are bare-bones scripts written to make willow's output compatible with Mountainsort
* There is no conversion of units, just raw data, so it is up to the user to know: 
  * The sample rate for the .json file (30000 Hz = default for leaf)
  * Scale factor for conversion of raw data to microvolts (0.195 according to Leaf Labs hdf52dat.m script)
* Probe geometry will vary between manufacturers and the number of probes/shanks/channels used
  * May need multiple probe geometries depending on the experimental setup

### Running Mountainsort
* Only runs on linux. Use conda environments to avoid installation errors
* See https://users.flatironinstitute.org/~magland/docs/mountainsort
* And https://github.com/flatironinstitute/mountainsort_examples/blob/master/README.md
* Conda installation instructions did not work for me as written, but this did:
	* conda install -c flatiron mountainlab 
	* conda install -c flatiron mountainlabmountainlab_pytools 
	* conda install -c flatiron mountainlabml_ephys 
	* conda install -c flatiron mountainlabml_ms3 
	* conda install -c flatiron mountainlabml_ms4alg 
	* conda install -c flatiron mountainlabml_pyms

