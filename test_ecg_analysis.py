# test_ecg_analysis.py
import pytest


def test_duration():
    from ecg_analysis import duration
    answer = duration([0.3, 0.8, 1.1, 1.5, 1.8, 2.2, 3.4])
    expected = 3.1
    assert answer == expected
