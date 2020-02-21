# ecg_analysis.py


def load_data():
    import csv
    f = "test_data/test_data30.csv"
    with open(f, newline='') as csvfile:
        ecgreader = csv.reader(csvfile, delimiter=' ')
        time, voltage = organize_data(ecgreader)
    return time, voltage


def organize_data(filereader):
    import logging
    logging.basicConfig(filename="ecg_analysis.log", filemode="w",
                        level=logging.INFO)
    time = list()
    voltage = list()
    for row in filereader:
        for r in row:
            line = r.split(',')
        # if either value missing, has non-numeric string, or is Nan
        # log error to log file, skip to next pair: missing_val()
        # w try/except
        try:
            time.append(float(line[0]))
        except ValueError:
            logging.error("Non-numeric string")
            continue
        # if voltage reading outside +/- 300 mV, add warning to log
        # file w name of test file and voltages exceeding
        # only once per file: bad_val()
        voltage.append(float(line[1]))
    # print(time)
    # print(voltage)
    return time, voltage


def analyze_trace(time, voltage):
    plot(time, voltage)


def plot(time, voltage):
    import matplotlib.pyplot as plt
    plt.plot(time, voltage)
    plt.show()


if __name__ == "__main__":
    t, v = load_data()
    analyze_trace(t, v)
