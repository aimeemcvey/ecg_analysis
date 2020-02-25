# ecg_analysis.py


def load_data(f):
    import csv
    with open(f, newline='') as csvfile:
        ecgreader = csv.reader(csvfile, delimiter=' ')
        time, voltage = organize_data(ecgreader, f)
    return time, voltage


def organize_data(filereader, file):
    import math
    import logging
    logging.basicConfig(filename="ecg_errors.log", filemode="w",
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
        except ValueError:
            logging.error("Time value bad/missing")
            continue
        try:
            vval = float(line[1])
        except ValueError:
            logging.error("Voltage value bad/missing")
            continue
        if math.isnan(tval) or math.isnan(vval):
            logging.error("Value NaN")
        time.append(tval)
        # if voltage reading outside +/- 300 mV, add warning to log
        if vval > 300 or vval < -300:
            high_voltages.append(vval)
        voltage.append(vval)
    if len(high_voltages) > 0:
        logging.warning("file={}: high voltages={}"
                        .format(file, high_voltages))
    return time, voltage


def analyze_trace(time, voltage, file):
    plot(time, voltage)
    timespan = duration(time)
    extremes = voltage_extremes(voltage)
    # beats = num_beats(voltage)
    # mean_hr = mean_hr_bpm(time, voltage):
    # beat_times = def beats(time)
    metrics = create_dict(timespan, extremes)  # add others later
    out_file = save_json(metrics, file)
    return out_file


def plot(time, voltage):
    import matplotlib.pyplot as plt
    plt.plot(time, voltage)
    plt.show()


def duration(time):
    timespan = time[-1] - time[0]
    return timespan


def voltage_extremes(voltage):
    minv = min(voltage)
    maxv = max(voltage)
    return minv, maxv


# def num_beats(voltage):
# def mean_hr_bpm(time, voltage):
# def beats(time)

def create_dict(timespan, extremes):
    metrics = {}
    metrics["duration"] = timespan
    metrics["voltage_extremes"] = extremes
    return metrics


def save_json(hr_dict, file):
    """Saves set of ECG data's key stats in JSON format

    ECG data is saved under 'test_data#.json' format
    with the following info: timespan (float),
    voltage_extremes (float tuple), num_beats (int),
    mean_hr_bpm (float), beats (list of ints)

    Args:
        hr_dict (dict): Patient information separated into keys-value pairs
        file (str): Filename and path with stem to be used as JSON filename

    Returns:
        JSON: ECG statistics for the individual patient
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
    file = "test_data/test_data31.csv"
    t, v = load_data(file)
    analyze_trace(t, v, file)
