"""Generated from Jupyter notebook: seismic earthquake

Magics and shell lines are commented out. Run with a normal Python interpreter."""


# --- code cell ---

# !pip install obspy  # Jupyter-only


# --- code cell ---

from obspy import UTCDateTime
from obspy.clients.fdsn import Client


def main():
    # Initialize the IRIS client
    client = Client("IRIS")
    # Define the time range for data retrieval
    start_time = UTCDateTime("2023-01-01T00:00:00")
    end_time = UTCDateTime("2023-01-01T01:00:00")
    # Specify the seismic station parameters
    network = "IU"  # Network code
    station = "ANMO"  # Station code
    location = "00"  # Location code
    channel = "BHZ"  # Channel code (e.g., BHZ for broadband high-gain vertical)
    # Retrieve the data
    st = client.get_waveforms(network, station, location, channel, start_time, end_time)
    # Display the retrieved data
    print(st)
    # Remove the instrument response to obtain ground displacement
    st.remove_response(output="DISP")
    # Apply a bandpass filter to isolate frequencies of interest
    st.filter("bandpass", freqmin=0.1, freqmax=10.0)
    # Plot the preprocessed data
    st.plot()
    from obspy.signal.trigger import classic_sta_lta, trigger_onset

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
        print(
            f"Event detected from {tr.stats.starttime + onset[0] / tr.stats.sampling_rate} "
            f"to {tr.stats.starttime + onset[1] / tr.stats.sampling_rate}"
        )
    import matplotlib.pyplot as plt

    # Extract and plot the first detected event
    if onsets:
        event_start = tr.stats.starttime + onsets[0][0] / tr.stats.sampling_rate
        event_end = tr.stats.starttime + onsets[0][1] / tr.stats.sampling_rate
        event_trace = tr.slice(starttime=event_start, endtime=event_end)
        # Plot the event
        plt.figure()
        plt.plot(event_trace.times("matplotlib"), event_trace.data, label="Detected Event")
        plt.xlabel("Time")
        plt.ylabel("Displacement (m)")
        plt.legend()
        plt.show()


    # --- code cell ---

    from obspy import UTCDateTime
    from obspy.clients.fdsn import Client

    # Initialize the IRIS client
    client = Client("IRIS")

    # Define the time range for data retrieval
    start_time = UTCDateTime("2025-02-12T00:00:00")
    end_time = UTCDateTime("2025-02-13T01:00:00")

    # Specify the seismic station parameters
    network = "IU"  # Network code
    station = "ANMO"  # Station code
    location = "00"  # Location code
    channel = "BHZ"  # Channel code

    # Retrieve the waveform data
    st = client.get_waveforms(network, station, location, channel, start_time, end_time)

    # Retrieve the station metadata (response information)
    inventory = client.get_stations(
        network=network,
        station=station,
        location=location,
        channel=channel,
        starttime=start_time,
        endtime=end_time,
        level="response",
    )

    # Print the retrieved data
    print(st)

    # Remove the instrument response to obtain ground displacement
    st.remove_response(inventory=inventory, output="DISP")

    # Apply a bandpass filter to isolate frequencies of interest
    st.filter("bandpass", freqmin=0.1, freqmax=10.0)

    # Plot the preprocessed data
    st.plot(outfile="waveform.png")


    # --- code cell ---

    from obspy.signal.trigger import classic_sta_lta, trigger_onset

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
        print(
            f"Event detected from {tr.stats.starttime + onset[0] / tr.stats.sampling_rate} "
            f"to {tr.stats.starttime + onset[1] / tr.stats.sampling_rate}"
        )
    import matplotlib.pyplot as plt

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
        plt.title("Detected Events")
        plt.savefig("detected_event.png")
        plt.show()


if __name__ == "__main__":
    main()
