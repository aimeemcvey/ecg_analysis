# ecg_analysis.py


def load_data():
    import csv
    f = "test_data/test_data23.csv"
    with open(f, newline='') as csvfile:
        ecgreader = csv.reader(csvfile, delimiter=' ')
        time, voltage = organize_data(ecgreader, f)
    return time, voltage


def organize_data(filereader, file):
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
        # log error, skip to next pair w try/except
        try:
            tval = float(line[0])
        except ValueError:
            logging.error("Value bad/missing")
            continue
        time.append(tval)
        # if voltage reading outside +/- 300 mV, add warning to log
        # file w name of test file and voltages exceeding, once per file
        vval = float(line[1])
        if vval > 0.3 or vval < -0.3:
            high_voltages.append(vval)
        voltage.append(vval)
    logging.warning("file = {}: high voltages = {}".format(file, high_voltages))
    return time, voltage


# def analyze_trace(time, voltage):
#     plot(time, voltage)
#
#
# def plot(time, voltage):
#     import matplotlib.pyplot as plt
#     plt.plot(time, voltage)
#     plt.show()


if __name__ == "__main__":
    t, v = load_data()
    # analyze_trace(t, v)
