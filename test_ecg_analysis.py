# test_ecg_analysis.py
import pytest


# def test_duration():
#     from ecg_analysis import duration
#     answer = duration([0.3, 0.8, 1.1, 1.5, 1.8, 2.2, 3.4])
#     expected = 3.1
#     assert answer == expected


@pytest.mark.parametrize("t, expected", [
    ([0.3, 0.8, 1.1, 1.5, 1.8, 2.2, 3.4], 3.1),
    ([0, 0.2, 0.7, 5.6, 9.3, 11.6], 11.6),
    ([1.1, 1.5, 1.7, 1.9, 2.5, 3.6], 2.5),
])
def test_duration(t, expected):
    from ecg_analysis import duration
    answer = duration(t)
    assert answer == expected
