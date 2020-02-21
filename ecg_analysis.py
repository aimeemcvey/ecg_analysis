# ecg_analysis.py


def load_data():
    import csv
    with open("test_data/test_data1.csv", newline='') as csvfile:
        ecgreader = csv.reader(csvfile, delimiter=' ')
        organize_data(ecgreader)


def organize_data(filereader):
    time = list()
    voltage = list()
    for row in filereader:
        for r in row:
            line = r.split(',')
        # if either value missing, has non-numeric string, or is Nan
        # log error to log file, skip to next pair
        time.append(float(line[0]))
        # if voltage reading outside +/- 300 mV, add warning to log
        # file w name of test file and voltages exceeding
        # only once per file
        voltage.append(float(line[1]))
    print(time)
    print(voltage)
    return time, voltage


if __name__ == "__main__":
    load_data()
