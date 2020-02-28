# ecg_analysis.py
import logging


def load_data(f):
    """Loads input file data into time and voltage lists

    The raw CSV ECG data must be loaded and arranged into
    lists of time and voltage for further analysis.

    Args:
        f (str): filename and path

    Returns:
        list: time data of the ECG strip
        list: voltage data of the ECG strip
    """
    import csv
    with open(f, newline='') as csvfile:
        ecgreader = csv.reader(csvfile, delimiter=' ')
        time, voltage, high_voltages = organize_data(ecgreader, f)
    return time, voltage, high_voltages


def organize_data(filereader, file):
    """Parses input file data into time and voltage lists

    The raw CSV ECG data must be read and bad values noted,
    including missing values, strings, NaNs, and voltages
    exceeding +/- 300 mV. A voltage this high or low likely
    indicates a problem with the recording of the ECG data.

    Args:
        filereader (_csv.reader): input data read in raw csv format
        file (str): filename and path

    Returns:
        list: time data of the ECG strip
        list: voltage data of the ECG strip
    """
    import math
    logging.basicConfig(filename="ecg_info.log", filemode="w",
                        level=logging.INFO)
    time = list()
    voltage = list()
    high_voltages = list()
    for row in filereader:
        for r in row:
            line = r.split(',')
        # val missing, non-numeric string, or NAN
        try:
            tval = float(line[0])
            vval = float(line[1])
        except ValueError:
            logging.error("Value bad/missing")
            continue
        if math.isnan(tval) or math.isnan(vval):
            logging.error("Value NaN")
        else:
            time.append(tval)
            voltage.append(vval)
        # if voltage reading outside +/- 300 mV, add warning to log
        if vval > 300 or vval < -300:
            high_voltages.append(vval)
    if len(high_voltages) > 0:
        logging.warning("file={}: high voltages={}"
                        .format(file, high_voltages))
    return time, voltage, high_voltages


def analyze_trace(time, voltage, file):
    """Analyzes ECG strip data for key information output as JSON

    An ECG records the electrical signals in the heart and is
    commonly used to detect and monitor heart problems. The
    recorded data is in the voltage-time format. Peaks and troughs
    indicate voltage changes that in turn indicate heart beats.
    These QRS waves can be analyzed for key information that aids
    in diagnosis.

    Args:
        time (list): time data of the ECG strip
        voltage (list): voltage data of the ECG strip
        file (str): filename and path with stem to be used as JSON filename

    Returns:
        JSON: ECG statistics for the individual file
    """
    logging.info("Starting analysis of new ECG trace")
    plot(time, voltage)
    timespan = duration(time)
    extremes = voltage_extremes(voltage)
    beats = num_beats(voltage)
    # mean_hr = mean_hr_bpm(time, voltage):
    # beat_times = def beats(time)
    metrics = create_dict(timespan, extremes)  # add others later
    out_file = save_json(metrics, file)
    return metrics
    return out_file


def plot(time, voltage):
    """Plots ECG strip data of voltage vs. time

    A plot of the ECG data allows for easy visualization
    of QRS waves, expected max and min voltage values, and
    expected number of heart beats.

    Args:
        time (list): time data of the ECG strip
        voltage (list): voltage data of the ECG strip

    Returns:
        pyplot: voltage-time plot of ECG strip
    """
    import matplotlib.pyplot as plt
    logging.info("Plotting ECG trace")
    plt.plot(time, voltage)
    plt.show()


def duration(time):
    """Calculates time span of ECG strip data

    The time span of the provided data indicates for how long
    the ECG test was administered and provides a benchmark
    for the number of expected heart beats.

    Args:
        time (list): time data of the ECG strip

    Returns:
        float: time duration of ECG strip
    """
    logging.info("Calculating time span of ECG trace")
    timespan = time[-1] - time[0]
    return timespan


def voltage_extremes(voltage):
    """Pinpoints min and max of voltages in ECG strip data

    The min and max voltages can provide information on
    abnormal polarization of the heart or point out abnormal
    data, whether too high or too low. Normal ECG amplitude
    reaches about 2.5-3.0 mV maximum.

    Args:
        voltage (list): voltage data of the ECG strip

    Returns:
        float tuple: (min, max) of lead voltages in file
    """
    logging.info("Identifying voltage extremes of ECG trace")
    minv = min(voltage)
    maxv = max(voltage)
    return minv, maxv


def num_beats(voltage):
    import scipy.signal
    logging.info("Calculating number of beats in ECG trace")
    peaks = scipy.signal.find_peaks(voltage, 0.5)
    peak_indices = peaks[0]
    print(peak_indices)
    num_peaks = len(peak_indices)
    print(num_peaks)

# def mean_hr_bpm(time, voltage):
    # logging.info("Calculating mean HR of ECG trace")
# def beats(time)
    # logging.info("Identifying time of beats in ECG trace")

def create_dict(timespan, extremes):
    """Creates metrics dictionary with key ECG information

    The metrics dictionary contains the the following info:
    timespan: float, voltage_extremes: float tuple, num_beats:
    int, mean_hr_bpm: float, beats: list of ints

    Args:
        timespan (float): time duration of ECG strip
        extremes (float tuple): (min, max) of lead voltages in file
        num_beats (int): number of detected beats in file
        mean_hr (float): average heart rate over file length
        beat_times (list of ints): times when beat occurred

    Returns:
        dict: metrics dictionary with ECG statistics of the input file
    """
    metrics = {}
    metrics["duration"] = timespan
    metrics["voltage_extremes"] = extremes
    print(metrics)
    return metrics


def save_json(hr_dict, file):
    """Saves set of ECG data's key stats in JSON format

    ECG data is saved under 'test_data#.json' format
    with the following info: timespan (float),
    voltage_extremes (float tuple), num_beats (int),
    mean_hr_bpm (float), beats (list of ints)

    Args:
        hr_dict (dict): patient information separated into keys-value pairs
        file (str): filename and path with stem to be used as JSON filename

    Returns:
        JSON: ECG statistics for the individual file
    """
    import json
    filepath_split = file.split('/')
    filename_csv = filepath_split[1]
    filename_stem = filename_csv.split('.')
    filename = filename_stem[0]
    filename = "{}.json" .format(filename)
    out_file = open(filename, 'w')
    json.dump(hr_dict, out_file)
    out_file.close
    return out_file


if __name__ == "__main__":
    file = "test_data/test_data1.csv"
    t, v, hv = load_data(file)
    analyze_trace(t, v, file)
