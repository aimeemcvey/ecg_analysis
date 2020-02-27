# test_ecg_analysis.py
import pytest


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


