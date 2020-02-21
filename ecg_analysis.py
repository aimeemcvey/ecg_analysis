# ecg_analysis.py


def load_data():
    import csv
    with open("test_data/test_data1.csv", newline='') as csvfile:
        ecgreader = csv.reader(csvfile, delimiter=' ')
        time = list()
        voltage = list()
        for row in ecgreader:
            for r in row:
                line = r.split(',')
            time.append(float(line[0]))
            voltage.append(float(line[1]))
        print(time)
        print(voltage)


if __name__ == "__main__":
    load_data()
