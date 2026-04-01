# Description: Short example for Time Series Analysis for Earthquake Detection Using Seismic Data.



from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.signal.trigger import classic_sta_lta, trigger_onset
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)



# Initialize the IRIS client
client = Client("IRIS")

# Define the time range for data retrieval
start_time = UTCDateTime("2025-01-01T00:00:00")
end_time = UTCDateTime("2025-01-01T01:00:00")

# Specify the seismic station parameters
network = "IU"       # Network code
station = "ANMO"     # Station code
location = "00"      # Location code
channel = "BHZ"      # Channel code

# Retrieve the waveform data
st = client.get_waveforms(network, station, location, channel, start_time, end_time)

# Retrieve the station metadata (response information)
inventory = client.get_stations(network=network, station=station, location=location,
                                channel=channel, starttime=start_time, endtime=end_time,
                                level="response")

# Print the retrieved data
logger.info(st)

# Remove the instrument response to obtain ground displacement
st.remove_response(inventory=inventory, output="DISP")

# Apply a bandpass filter to isolate frequencies of interest
st.filter("bandpass", freqmin=0.1, freqmax=10.0)

# Plot the preprocessed data
st.plot()

1 Trace(s) in Stream:
IU.ANMO.00.BHZ | 2025-02-12T00:00:00.019538Z - 2025-02-13T00:59:59.994538Z | 40.0 Hz, 3600000 samples
Selection deleted

# Select the first trace in the stream
tr = st[0]
# Apply the STA/LTA algorithm
sta_lta = classic_sta_lta(tr.data, nsta=500, nlta=10000)
# Define trigger thresholds
trigger_on = 3.5
trigger_off = 1.0
# Identify trigger onsets
onsets = trigger_onset(sta_lta, trigger_on, trigger_off)
# Print detected event onsets
for onset in onsets:
    logger.info(f"Event detected from {tr.stats.starttime + onset[0] / tr.stats.sampling_rate} "
          f"to {tr.stats.starttime + onset[1] / tr.stats.sampling_rate}")
# Extract and plot the first detected event
if len(onsets) > 0:
    event_start = tr.stats.starttime + onsets[0][0] / tr.stats.sampling_rate
    event_end = tr.stats.starttime + onsets[0][1] / tr.stats.sampling_rate
    event_trace = tr.slice(starttime=event_start, endtime=event_end)
    # Plot the event
    plt.figure()
    plt.plot(event_trace.times("matplotlib"), event_trace.data, label="Detected Event")
    plt.xlabel("Time")
    plt.ylabel("Displacement (m)")
    plt.legend()
    plt.savefig("detected_event.png") 
    plt.show()
