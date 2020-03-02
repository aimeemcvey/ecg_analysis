# test_ecg_analysis.py
import pytest
import math


def test_load_data_missing_vals():
    from ecg_analysis import load_data
    file = "test_data/test_data_load_test_missing_vals.csv"
    ans1, ans2, ans3 = load_data(file)
    time = ([0.0, 0.003, 0.006, 0.008, 0.011, 0.014, 0.017, 0.019, 0.022,
             0.025, 0.028, 0.033, 0.036, 0.039, 0.042, 0.044, 0.047, 0.05])
    voltage = ([-0.145, -0.145, -0.145, -0.145, -0.145, -0.145, -0.145,
                -0.145, -0.12, -0.13, -0.145, -0.16, -0.155, -0.16, -0.175,
                -0.18, -0.185, -0.17])
    high_voltages = ([])
    expected = time, voltage, high_voltages
    answer = ans1, ans2, ans3
    assert answer == expected


def test_load_data_nan():
    from ecg_analysis import load_data
    file = "test_data/test_data_load_test_nan.csv"
    ans1, ans2, ans3 = load_data(file)
    time = ([0.0, 0.003, 0.006, 0.008, 0.014, 0.017, 0.019, 0.022,
             0.025, 0.028, 0.030, 0.033, 0.036, 0.039, 0.042, 0.044,
             0.05, 0.053])
    voltage = ([-0.145, -0.145, -0.145, -0.145, -0.145, -0.145,
                -0.145, -0.12, -0.13, -0.145, -0.15, -0.16, -0.155,
                -0.16, -0.175, -0.18, -0.17, -0.18])
    high_voltages = ([])
    expected = time, voltage, high_voltages
    answer = ans1, ans2, ans3
    assert answer == expected


def test_load_data_excess_voltage():
    from ecg_analysis import load_data
    file = "test_data/test_data_load_test_excess_voltage.csv"
    ans1, ans2, ans3 = load_data(file)
    time = ([0.0, 0.003, 0.006, 0.008, 0.010, 0.014, 302.0, 0.019, 0.022,
             0.025, 0.028, 0.030, 0.033, 0.036, 0.039, 0.042, 0.044, 0.047,
             0.05, 0.053])
    voltage = ([-0.145, -0.145, -0.145, -0.145, -0.145, -0.145, -0.145,
                -0.145, -0.12, -0.13, -0.145, -0.15, -0.16, -0.155, -0.16,
                -0.175, -0.18, -301.0, -0.17, -0.18])
    high_voltages = ([-301.0])
    expected = time, voltage, high_voltages
    answer = ans1, ans2, ans3
    assert answer == expected


def test_analyze_trace():
    from ecg_analysis import analyze_trace
    from ecg_analysis import load_data
    file = "test_data/test_data2.csv"
    t, v, hv = load_data(file)
    answer = analyze_trace(t, v, file)
    expected = {"duration": 27.775, "voltage_extremes": (-0.59, 1.375),
                "num_beats": 32, "mean_hr_bpm": 69, "beats":
                    [0.319, 1.192, 2.019, 2.911, 3.844, 4.758, 5.658,
                     6.528, 7.436, 8.258, 9.214, 10.175, 11.047, 11.9,
                     12.85, 13.692, 14.603, 15.517, 16.433, 17.289,
                     18.181, 18.975, 19.886, 20.775, 21.675, 22.561,
                     23.375, 24.272, 25.117, 25.936, 26.789, 27.65]
                }
    assert answer == expected


def test_analyze_trace_2():
    from ecg_analysis import analyze_trace
    from ecg_analysis import load_data
    file = "test_data/test_data8.csv"
    t, v, hv = load_data(file)
    answer = analyze_trace(t, v, file)
    expected = {"duration": 27.775, "voltage_extremes": (-3.105, 1.975),
                "num_beats": 33, "mean_hr_bpm": 71, "beats":
                    [0.331, 0.822, 1.578, 2.531, 3.436, 4.283, 5.142,
                     5.881, 6.794, 7.647, 8.514, 9.383, 10.233, 11.119,
                     11.942, 12.753, 13.586, 14.447, 15.328, 16.197,
                     17.058, 17.886, 18.731, 19.55, 20.397, 21.2, 22.161,
                     23.017, 23.819, 24.567, 25.483, 26.372, 27.258]
                }
    assert answer == expected


@pytest.mark.parametrize("t, expected", [
    ([0.3, 0.8, 1.1, 1.5, 1.8, 2.2, 3.4], 3.1),
    ([0, 0.2, 0.7, 5.6, 9.3, 11.6], 11.6),
    ([1.1, 1.5, 1.7, 1.9, 2.5, 3.6], 2.5),
])
def test_duration(t, expected):
    from ecg_analysis import duration
    answer = duration(t)
    assert answer == expected


@pytest.mark.parametrize("v, expected", [
    ([0, 0.1, -0.5, 1.2, 2.4, -3.4, 1.0, 2.1], (-3.4, 2.4)),
    ([-0.1, 0.8, -5.3, 1.8, 3.5, -3.3, 2.4, -3.4], (-5.3, 3.5)),
    ([0, 0, 0, 0, 0], (0, 0)),
])
def test_voltage_extremes(v, expected):
    from ecg_analysis import voltage_extremes
    answer = voltage_extremes(v)
    assert answer == expected


def test_num_beats():
    from ecg_analysis import num_beats
    from ecg_analysis import load_data
    from ecg_analysis import voltage_extremes
    file = "test_data/test_data10.csv"
    t, v, hv = load_data(file)
    answer, peaks = num_beats(v, t)
    expected = 44
    assert answer == expected


@pytest.mark.parametrize("file, expected", [
    ("test_data/test_data4.csv", 32),
    ("test_data/test_data12.csv", 19),
    ("test_data/test_data17.csv", 19),
    ("test_data/test_data29.csv", 19),
    ("test_data/test_data32.csv", 19),
    ("test_data/test_data25.csv", 32),
    ("test_data/test_data26.csv", 55),
])
def test_num_beats_ext(file, expected):
    from ecg_analysis import num_beats
    from ecg_analysis import load_data
    from ecg_analysis import voltage_extremes
    t, v, hv = load_data(file)
    answer, peaks = num_beats(v, t)
    assert (1.10 * expected) > answer > (0.90 * expected)


@pytest.mark.parametrize("file, expected", [
    ("test_data/test_data10.csv", 95),
    ("test_data/test_data17.csv", 78),
    ("test_data/test_data28.csv", 73),
])
def test_mean_hr_bpm(file, expected):
    from ecg_analysis import mean_hr_bpm
    from ecg_analysis import load_data
    from ecg_analysis import voltage_extremes
    from ecg_analysis import num_beats
    from ecg_analysis import duration
    t, v, hv = load_data(file)
    nbeats, peaks = num_beats(v, t)
    t_in_s = duration(t)
    answer = mean_hr_bpm(nbeats, t_in_s)
    assert answer == expected


def test_beats():
    from ecg_analysis import beats
    from ecg_analysis import load_data
    from ecg_analysis import num_beats
    file = "test_data/test_data10.csv"
    t, v, hv = load_data(file)
    nbeats, peaks = num_beats(v, t)
    answer = beats(peaks, t)
    expected = [0.3, 1.003, 1.636, 2.233, 2.961, 3.625, 4.217, 5.011,
                5.594, 6.256, 6.856, 7.494, 8.058, 8.764, 9.361,
                10.011, 10.642, 11.275, 11.936, 12.494, 13.133, 13.683,
                14.292, 14.936, 15.589, 16.219, 16.847, 17.431, 18.058,
                18.708, 19.267, 19.867, 20.489, 21.175, 21.839, 22.458,
                23.086, 23.733, 24.364, 24.969, 25.653, 26.228, 26.886,
                27.597]
    assert answer == expected


def test_beats_2():
    from ecg_analysis import beats
    from ecg_analysis import load_data
    from ecg_analysis import num_beats
    file = "test_data/test_data22.csv"
    t, v, hv = load_data(file)
    nbeats, peaks = num_beats(v, t)
    answer = beats(peaks, t)
    expected = [0.352, 1.424, 2.528, 3.624, 4.62, 5.716, 6.72, 7.824,
                8.876, 9.976, 11.04, 12.04, 13.148, 14.252, 15.308,
                16.344, 17.472, 18.544, 19.556, 20.696, 21.804, 22.868,
                23.948, 25.06, 26.064, 27.196, 28.284, 29.392, 30.432,
                31.56, 32.704, 33.804, 34.848, 35.992, 37.068, 38.124,
                39.224]
    assert answer == expected


def test_create_dict():
    from ecg_analysis import create_dict
    timespan = 4.5
    extremes = (-3.5, 1.3)
    numbeats = 31
    mean_hr = 63
    beat_times = [0.1, 0.3, 0.5]
    answer = create_dict(timespan, extremes, numbeats,
                         mean_hr, beat_times)
    expected = {"duration": 4.5, "voltage_extremes": (-3.5, 1.3),
                "num_beats": 31, "mean_hr_bpm": 63,
                "beats": [0.1, 0.3, 0.5]}
    assert answer == expected
