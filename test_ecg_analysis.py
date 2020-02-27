# test_ecg_analysis.py
import pytest
import math


def test_load_data():
    # missing tval, vval, nan, -301
    from ecg_analysis import load_data
    file = "test_data/test_data_load_test.csv"
    ans1, ans2, ans3 = load_data(file)
    time = ([0.0, 0.003, 0.006, 0.008, 0.011, 0.014, 0.017, 0.019, 0.022,
            0.025, 0.028, 0.033, 0.036, 0.042, 0.044, 0.047, 0.05])
    voltage = ([-0.145, -0.145, -0.145, -0.145, -0.145, -0.145, -0.145,
               -0.145, -0.12, -301.0, -0.145, -0.16, -0.155, -0.175,
               -0.18, -0.185, -0.17])
    high_voltages = ([-301.0])
    expected = time, voltage, high_voltages
    print(expected)
    answer = ans1, ans2, ans3
    print(answer)
    assert answer == expected


def test_analyze_trace():
    from ecg_analysis import analyze_trace
    time = ([0.1, 0.3, 0.5, 0.9, 1.5, 1.7, 1.9, 2.3, 2.6,
             3.1, 3.6, 3.8, 4.0, 4.3])
    voltage = ([-0.3, -0.9, -1.4, -1.7, -1.4, 0.1, 0.5, 0.7, 0.1,
                1.3, 0.6, 1.8, 3.5, 2.0])
    file = "test_data/test_data_madeup.csv"
    answer = analyze_trace(time, voltage, file)
    expected = {"duration": 4.2, "voltage_extremes": (-1.7, 3.5)}
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


def test_create_dict():
    from ecg_analysis import create_dict
    timespan = 4.5
    extremes = (-3.5, 1.3)
    answer = create_dict(timespan, extremes)
    expected = {"duration": 4.5, "voltage_extremes": (-3.5, 1.3)}
    assert answer == expected
