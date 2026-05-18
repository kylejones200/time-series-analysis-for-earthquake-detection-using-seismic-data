"""Generated from Jupyter notebook: seismic earthquake

Magics and shell lines are commented out. Run with a normal Python interpreter."""

import matplotlib.pyplot as plt
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.signal.trigger import classic_sta_lta, trigger_onset


def initialize_the_iris_client() -> None:
    client = Client("IRIS")
    start_time = UTCDateTime("2023-01-01T00:00:00")
    end_time = UTCDateTime("2023-01-01T01:00:00")
    network = "IU"
    station = "ANMO"
    location = "00"
    channel = "BHZ"
    st = client.get_waveforms(network, station, location, channel, start_time, end_time)
    print(st)
    st.remove_response(output="DISP")
    st.filter("bandpass", freqmin=0.1, freqmax=10.0)
    st.plot()
    tr = st[0]
    sta_lta = classic_sta_lta(tr.data, nsta=500, nlta=10000)
    trigger_on = 3.5
    trigger_off = 1.0
    onsets = trigger_onset(sta_lta, trigger_on, trigger_off)
    for onset in onsets:
        print(
            f"Event detected from {tr.stats.starttime + onset[0] / tr.stats.sampling_rate} to {tr.stats.starttime + onset[1] / tr.stats.sampling_rate}"
        )

    if onsets:
        event_start = tr.stats.starttime + onsets[0][0] / tr.stats.sampling_rate
        event_end = tr.stats.starttime + onsets[0][1] / tr.stats.sampling_rate
        event_trace = tr.slice(starttime=event_start, endtime=event_end)
        plt.figure()
        plt.plot(
            event_trace.times("matplotlib"), event_trace.data, label="Detected Event"
        )
        plt.xlabel("Time")
        plt.ylabel("Displacement (m)")
        plt.legend()
        plt.show()


def initialize_the_iris_client_2() -> None:
    client = Client("IRIS")
    start_time = UTCDateTime("2025-02-12T00:00:00")
    end_time = UTCDateTime("2025-02-13T01:00:00")
    network = "IU"
    station = "ANMO"
    location = "00"
    channel = "BHZ"
    st = client.get_waveforms(network, station, location, channel, start_time, end_time)
    inventory = client.get_stations(
        network=network,
        station=station,
        location=location,
        channel=channel,
        starttime=start_time,
        endtime=end_time,
        level="response",
    )
    print(st)
    st.remove_response(inventory=inventory, output="DISP")
    st.filter("bandpass", freqmin=0.1, freqmax=10.0)
    st.plot(outfile="waveform.png")


def select_the_first_trace_in_the_stream() -> None:
    tr = st[0]
    sta_lta = classic_sta_lta(tr.data, nsta=500, nlta=10000)
    trigger_on = 3.5
    trigger_off = 1.0
    onsets = trigger_onset(sta_lta, trigger_on, trigger_off)
    for onset in onsets:
        print(
            f"Event detected from {tr.stats.starttime + onset[0] / tr.stats.sampling_rate} to {tr.stats.starttime + onset[1] / tr.stats.sampling_rate}"
        )

    if len(onsets) > 0:
        event_start = tr.stats.starttime + onsets[0][0] / tr.stats.sampling_rate
        event_end = tr.stats.starttime + onsets[0][1] / tr.stats.sampling_rate
        event_trace = tr.slice(starttime=event_start, endtime=event_end)
        plt.figure()
        plt.plot(
            event_trace.times("matplotlib"), event_trace.data, label="Detected Event"
        )
        plt.xlabel("Time")
        plt.ylabel("Displacement (m)")
        plt.title("Detected Events")
        plt.savefig("detected_event.png")
        plt.show()


def main() -> None:
    initialize_the_iris_client()
    initialize_the_iris_client_2()
    select_the_first_trace_in_the_stream()


if __name__ == "__main__":
    main()
