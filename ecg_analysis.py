# ecg_analysis.py


def load_data():
    import csv
    f = "test_data/test_data31.csv"
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
        logging.warning("file={}: high voltages={}".format(file, high_voltages))
    return time, voltage


def analyze_trace(time, voltage):
    metrics = {}
    # trace[x] later
    plot(time, voltage)
    timespan = duration(time)
    extremes = voltage_extremes(voltage)
    metrics["duration"] = timespan
    metrics["voltage_extremes"] = extremes
    print(metrics)


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


if __name__ == "__main__":
    t, v = load_data()
    analyze_trace(t, v)
