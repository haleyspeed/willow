# User guide for Leaf Labs Willow System

## Rationale
Ultra-high density recordings from the Willow system must be scaled, filtered, and transformed before analysis in spike sorting scripts like Mountainsort or Kilosort. This collection of Jupyter notebooks does all of this plus modules for subtracting baseline probe noise from experimental data and reformatting scripts for use with Kilosort or Mountainsort. All except Mountainsort or Kilosort themselves can be run on Mac OS, as well as Ubuntu linux. The scripts have been optimized to run on high-end laptops instead of HPCs or workstations for greater flexibility.

## System requirements:
 - 1TB HD
 - i7 processor or equivalent
 - 16 GB DDR4 RAM
 - Ubuntu OS (for Mountainsort)
 - Mac OS or Ubuntu OS for all other scripts
 - Python3.x and jupyter notebooks installed (see Appendix)

## Configure a Python session
 1. Download the latest versions of the analysis files (.ipynb) from https://github.com/haleyspeed/willow
 2. Open a new Terminal
  - Either click on the Terminal icon in the doc or click on the grid-like button on the dock and choose the "All" tab then the "Terminal" icon
 3. Navigate to the parent folder of the leaf_env folder, activate the leaf_env kernel, then open jupyter notebook. This should open up your browser and show you the willow directory. Navigate it just like a normal file explorer window to find your experiment folder with the .h5 files.
     - $ cd willow/data/leaf_env
     - $ source leaf_env/bin/Activate
     - $ jupyter notebook

      *There should be one folder per experiment,
      even if that means multiple subdirectories.*

4. Run each cell by clicking in the cell then clicking on the "run" button on the toolbar. Wait for it to finish before you move to the next cell.
 - `In [*]` means the cell is running
 - `In [1]` means the cell has completed
5. All data generated by the scripts are saved in the same folder as the `.h5` and  `.ipynb` files
6. Scripts (IPython Notebooks) are designed to run on standard laptops and desktops, so recordings are broken down by shank. Theoretically, a 256 channel probe with 4 shanks could have 64 channels. In reality, most probe manufactures reserve some recording sites for wiring, resulting in dead sites. You need a probe map to determine what the `row_num` should be. This also means that instead of 64 channels of data on a probe, you'll probably only get 61 active channels.  An example:
 - Probe map indicates dead channels in column 1 row 3, column 2 row 1, and column 3 row 5.
  - `row_num = [[:3,4:], [1:], [:5,6:]]`
  - Instead of 3 integers in row_num, we have 3 lists.
  - Remember that Python starts numbering at 0, not 1
  - Remember that lists are exclusive - the last number in a list is not included in the function.
  - Ranges in lists are defined by `[:]`. A number to the left of the colon means 'start here' and the numbers to the right mean 'stop here and don't include this one'

## Analysis Pipeline
Analysis will consist of 5 parts:
1. `h5_probe.ipynb` -- Probe quality control (recorded in saline with all proper grounds). Measures impedance, scales raw data to microvolts, and analyzes baseline probe noise. Traces (1 second long) from each channel can be subtracted from the experimental data in `h5_subtractor.ipynb` to increase signal/noise.
2. `h5_explorer.ipynb` -- Scales raw data to microvolts. Finds an appropriate window (0.5-1 second) for clustering analysis in mountainsort or to make example figures of raw traces. Band pass filters data at 450-5000 Hz and saves the filtered traces.
3. `h5_subtractor.ipynb` (optional) -- Subtracts 1s trace from saline probe recording (analyzed in `h5_probe.ipynb`) from experimental trace.
4. `h5_to_mda.ipynb` -- Reads in scaled, subtracted (optional), and filtered data from h5_explorer or h5_subtractor and converts it to a mountainsort data file (.mda)
5. `willow_ms.ipynb` - A version of mountainsort4 modified specifically for the leaf system.


* All of these files are assumed to be in the same directory as the impedance, experiment, and probe recording h5 files. You should have 1 folder per experiment, or at the very least one folder per mouse.
* Make copies of the .ipynb python notebooks for EVERY experiment. This is "showing your work" and counts as a lab notebook. Each analysis should be kept as a standalone record even after you've deleted the .h5 files to clear hard drive space. If you have 4 shanks in one recording, you will have 4 copies  of each script, so name them something like 'h5_probe_shank1.ipynb' or 'h5_probe_64.ipynb' so that you know which channels are being analyzed in each script.
* You will not be able to analyze more than 64 channels at a time on a normal laptop. A high-end workstation might allow for 256, but for all 1000 channels, you will need to work on the HPC (and probably convert the python notebooks to .py scripts if jupyter is not installed on the HPC -- Mark Carlson, Glenn Morton, and Sean Taylor in Bioinformatics can help with this.)


## Analyze probe quality
#### User input

- `impfile` -- .h5 impedance file for the probe. Should be measured in saline with grounding between the probe and the probe adapter, as well as a silver wire ground also in the same saline bath.
- `basefile` -- .h5 recording with the probe and ground wire in saline, mimicking a real experiment in the brain. Be sure to note the filename and/or time of recording so you don't mistake it for a real experiment later in analysis.
- `fs` -- sample rate. Default is 30000 Hz for the leaf.
- `chan_range` -- default is 64 channels/shank for Ingrid's IDT probes in testing. `chan_range` is a list variable with two values, the first channel to analyze and the last channel to analyze, enclosed in brackets. Python starts numbering at 0, so channels 1-64 on the probe would be 0-64 in python code. Default is chan_range = [0,64] for shank1 on a 256 channel, 4-shank probe.
- `col_num` -- is the number of columns per shank. This can change with every probe, so check the probe map. In testing with IDT probes, the default was 3.
- `row_num` -- The number of rows per column on the shank. This is another list variable with the same number of values as the number of columns. In testing, we had 3 columns per shank with 21 rows in column1, 20 rows in column 2, and 21 rows in column3 so `row_num = [21,20,21]`

#### Running the script
- Enter the user input into the first box then click the `Run` button in the toolbar or `shift + Enter` from the keyboard.
- Do the same for each subsequent box.
- If a box is running, there will be a star in brackets in the upper left `In [\*]`. Wait for it to finish before going to the next box or you'll get memory errors and dead kernels.
- Many of these steps can take up to an hour, depending on the processor and memory of the computer running the script. As long as the `[\*]` is present and there is no `dead kernel` warning in the top right of the jupyter window, it's still chugging along.
- When each box finishes, it will replace the `[\*]` with a number `[2]`. The number indicates the order the box was executed. Every time you restart the kernel, this will reset. It allows people to come behind you and see the sequence of steps in your work, so keep that in mind as you go (i.e. NIH audits). In testing, the scripts were written to be sequential, so that they must be run in order on the first go, but this does not protect against subsequent runs if the kernel is not restarted between runs.
- To restart the kernel, go to the file menu in the jupyter window `Kernel --> Restart and Clear All Output`

#### Output
- `Filename_impedance.png` - Scatter plot of impedance for each channel
- `Filename_probe.h5`- A new h5 probe file containing scaled filtered and unfiltered traces (full length) and descriptive statistics on filtered and unfiltered noise levels on the probe. The .h5 file is structured like a directory with 5 "folders":
 1. `x` - x values (time in datapoints)
 2. `unfiltered_y` - scaled, unfiltered y values (microvolts)
 3. `filtered_y` - scaled, bandpass filtered y values (microvolts)
 4. `unfiltered_stats` - Noise analysis of scaled, unfiltered data.
   - Columns 1-4 = mean, median, standard deviation, range.
   - Rows = channel number
 5. `filtered_stats`  - Noise analysis of scaled, filtered data.
   - Columns 1-4 = mean, median, standard deviation, range.
   - Rows = channel number


- `Filename_probe_unfiltered.png` - 1 second traces of unfiltered data from all channels on the probe. Traces are arranged in the order they appear on the probe. Depends on accurate user input in the `col_num` and `row_num` variables in the first step.
- `Filename_probe_filtered.png` - 1 second traces of filtered data from all channels on the probe. Traces are arranged in the order they appear on the probe. Depends on accurate user input in the `col_num` and `row_num` variables in the first step.


## Analyze Recording Quality and Filter Experimental Data
#### User input
- `datafile` - your h5 experiment file (brain recording)
- `fs` - sample rate, default is 30000 Hz for willow
- `chan_num` = # channels to analyze. 64 is safest unless running on a workstation. The test workflow is set up to pre-process one shank at a time (64 channels). The variable is a list with two numbers: The starting channel and the ending channel, so if you want to analyze channels 1-64, `chan_num = [0,64]`
- `col_num` -- is the number of columns per shank. This can change with every probe, so check the probe map. In testing with IDT probes, the default was 3.
- `row_num` -- The number of rows per column on the shank. This is another list variable with the same number of values as the number of columns. In testing, we had 3 columns per shank with 21 rows in column1, 20 rows in column 2, and 21 rows in column3 so `row_num = [21,20,21]`


#### Running the script
- same as for "Analyzing Probe Quality" in the previous section

#### Output
- filename_filtered_64.h5 - filtered data (bandpass, order = 6, 450-5000 Hz) saved with two keys:
  1. `x` - time in datapoints
  2. `y` - scaled and filtered data in microvolts (64 columns, one for each channel)
  3. `filtered_stats`  - Noise analysis of scaled, filtered data.
    - Columns 1-4 = mean, median, standard deviation, range.
    - Rows = channel number-
  4. `unfiltered_stats` - Noise analysis of scaled, unfiltered data.
    - Columns 1-4 = mean, median, standard deviation, range.
    - Rows = channel number


- `filename_unfiltered_64.png` - Grid image of all unfiltered traces from 1 shank arranged according to the probe map (physical representation). Arrangement is based off of `chan_num`, `col_num`, and `row_num` in User Input, so make sure these are correct for your probe/shank. They will change with probe design and manufacturer. the "\_64" in the new filename will be the second number in the `chan_num` list variable.

- `filename_filtered_64.png` - same as for the unfiltered plot except with the bandpass filtered data.

## (Optional) Subtract probe noise from experimental files
#### User Input
- `datafile` - filtered experimental file from h5_explorer.ipynb
- `basefile` - filtered probe file from h5_probe.ipynb
- `fs` - sample rate (30000 Hz default)
- `col_num` -- is the number of columns per shank. Should be the same as in `h5_explorer.ipynb` and `h5_probe.ipynb`
- `row_num` -- The number of rows per column on the shank. Should be the same as in `h5_explorer.ipynb` and `h5_probe.ipynb`


#### Running the script
- Step through box-by-box in order, waiting for the current one to finish before going to the next, as for `h5_explorer.ipynb` and `h5_probe.ipynb`
- The subtraction step is a long one.

#### Output
- `filename_subtracted_64.h5` - Contains two datasets (keys):
  - `x` = time in datapoints
  - `subtracted` - y data of the subtracted experiment file (microvolts)
- `filename_subtracted_64.png` -  Raw traces (1 second) from subtracted data plotted according to the probe map.  

# User guide for MountainSort4 with Willow

## Rationale
Mountainsort is an alternative to Kilosort for spike-sorting ultra-high-density neural recordings. Besides being open source and not tied to Matlab, it has the advantage of setting the size of the clustering (neighborhood) radius. The mountainsort files are distributed in many places, mostly in development stages. This is the process I found for successfully installing and running a stable mountainsort script, based off of the examples given at https://github.com/flatironinstitute/mountainsort_examples/tree/master/jupyter_examples

## System requirements:
 - 1TB HD
 - i7 processor or equivalent
 - 16 GB DDR4 RAM
 - Ubuntu OS (for Mountainsort)
 - Python3.6 with anaconda and jupyter notebooks installed (see Appendix)

## Setting up the conda environment for MountainSort
 - Download the linux (Debian) 64 bit anaconda installer for Python 3.x
    - It will be an .sh file
 - Open a terminal and execute the following command to install prereqs
  - $ `apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6`
 - Navigate to the folder with the .sh file
  - Run the .sh file with the command where Anaconda3.... is the filename of the .sh file
   - $ `bash ~/Downloads/Anaconda3.....sh`
   - Follow the instructions and do a default install
- Create a new conda environment
   - (leaf_conda) $ `conda create --name leaf_conda python=3.6`
   - (leaf_conda) $ `conda activate leaf_conda`

## Install MountainSort4 (condensed from MS github)
- Execute the following commands in order:
 - (leaf_conda) $ `conda config --add channels conda-forge`
 - (leaf_conda) $ `conda config --set channel_priority strict`
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge mountainlab`
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge mountainlab_pytools `
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge ml_ephys`
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge ml_ms3`
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge ml_ms4alg`
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge ml_pyms`


- Check the installation
 - (leaf_conda) $ `ml-list-processors`
  - If successful you'll get a long list
  - If you get anything else, repeat the steps above until it works
  - For additional troubleshooting resources, see these links:
   - https://docs.anaconda.com/anaconda/install/linux/
   - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment
   - https://conda-forge.org/
   - https://github.com/flatironinstitute/mountainsort_examples/blob/master/README.md


- Install visualization tools
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge ephys-viz`


- Install jupyter compatibility packages
 - (leaf_conda) $ `conda install -c flatiron -c conda-forge spikeforestwidgets`
 - (leaf_conda) $ `jupyter nbextension enable --py --sys-prefix jp_proxy_widget`
 - (leaf_conda) $ `jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build`
 - (leaf_conda) $ `jupyter labextension install jp_proxy_widget --no-build`
 - (leaf_conda) $ `jupyter lab build`
 - (leaf_conda) $ `conda install ipykernel`

## Running mountainsort.ipynb
- Copy `mountainsort.ipynb` to the experiment directory
- Copy the `sorterfiles` folder (https://www.dropbox.com/sh/b23my6oonlw41y4/AAB4QojtxpJmplHOZ46Sm30ta?dl=0) into the experiment folder as a subfolder
- Make another subfolder in your experiment's directory named `dataset`
  - Add your `raw.mda`, `geom.csv`, and `params.json` files to the `dataset` folder
 - First test the set by making sure the following lines are not commented out (i.e. don't have a # sign in front of them)
    `with Pipeline:
    synthesize_dataset(dsdir,M=4,duration=600,average_snr=8)`
 - Run each box in turn, pay attention to the pipeline status to make sure it's still Running
 - If it runs with no errors, delete any files in the `dataset` subfolder, copy over your `raw.mda`, `geom.csv`, and `params.json` files to the dataset folder, clear the kernal and retart the script (shut it down if you have to then reopen).
 - If you get an error regarding `firings_true.mda` does not exist, or something to that effect, no events were found.


# Appendix

## Setting up a new linux machine to run analysis programs
- Update and Upgrade the sudo app management application
  - $ `sudo apt-get update`
  - $ `sudo apt-get upgrade`
- Install python3 and its graphical user interface bits "tk"
  - $ `sudo apt-get install python3`
  - $ `sudo apt-get install python3-tk`
- Upgrade the pip python pacakge management app
  - $ `python3 -m pip install --upgrade pip`
- Create virtual environments for python3
  - $ `python3 -m pip install virtualenv`
  - $ `python3 -m virtualenv leaf_env`
- Activate the virtual environment
  - $ `source leaf_env/bin/activate`
- Install all necessary python site_packages
  - $ `python3 -m pip install scikit-learn matplotlib pandas numpy h5py jupyterlab ipykernel numpydoc`
  - These can be installed individually, line-by-line, as well:
   - $ `python3 -m pip install scikit-learn`
   - $ `python3 -m pip install matplotlib`
   - $ `python3 -m pip install pandas`
   - $ `python3 -m pip install numpy`
   - $ `python3 -m pip install h5py`
   - $ `python3 -m pip install jupyterlab`
   - $ `python3 -m pip install ipykernel`
- Register the jupyter notebook kernel to run in your leaf_env virtual environments
 - $ `python3 -m ipykernel install --user --name leaf_env --display-name "Python3 (leaf_env)"`
- Copy the `mlpy` folder from the github or dropbox into the `leaf_env/lib/Python3.7/site_packages folder `


## Troubleshooting
- Error: 'Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.plt.show()'
 - Install "tk" - the graphical user interface bits of python
  - $ `sudo apt-get install python3-tk`
- No module named spikeinterface
  - From the terminal, navigate to the parent directory of the leaf_env folder
   - $ source leaf_env/bin/Activate
   - $ python3 -m pip install spikeinterface
- Exception: Incompatible dimensions between geom.csv and timeseries file 65 <> 63 (or similar)
 - Check that your input file to h5_to_mda.ipynb and output raw.mda and geom.csv all have the same number of channels. This is usually a list error (forgetting that in a list the last channel will not be inlcuded) or forgetting that python starts numbering at 0 rather than 1.