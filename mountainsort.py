# Imports
import spikeinterface as si
import spiketoolkit as st
import spikewidgets as sw
import spikeinterface.extractors as se

# Read in the recording from the dataset/ directory
din = "/home/willow/Desktop/MountainSort/scripts/ms_test"
recording = se.MdaRecordingExtractor(folder_path = din)

# Run the spike sorting
sorting = st.sorters.mountainsort4(
    recording=recording,
    detect_sign=-1,
    adjacency_radius=50,
    freq_min=300, freq_max=6000,
    whiten=True,
    clip_size=50,
    detect_threshold=3,
    detect_interval=10,
    noise_overlap_threshold=0.15
)

# Save the results as firings.mda
si.MdaSortingExtractor.writeSorting(sorting=sorting, save_path='firings.mda')

# View the average waveforms
sw.UnitWaveformsWidget(recording=recording, sorting=sorting).plot()
