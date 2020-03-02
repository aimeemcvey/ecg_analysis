# ECG Analysis Assignment [![Build Status](https://travis-ci.com/BME547-Spring2020/ecg-analysis-aimeemcvey.svg?token=uYZMqDdwHppZCbLZESzP&branch=master)](https://travis-ci.com/BME547-Spring2020/ecg-analysis-aimeemcvey)
This project analyzes an ECG strip's voltage-time data for several key values: duration, voltage extremes, number and timing of beats, and average heart rate. These values are output as a JSON file for each set of ECG data.

The ECG is the most important test for determining heart health, including heart rate, electrical conduction abnormalities, and detection of atherosclerosis. It can also lead to diagnoses of cardiac abnormalities including valvular heart disease, cardiomyopathy, pericarditis, and hypertension. The ECG itself is a plot of voltage versus time, where the wave is deflected a given distance based on the voltage potential difference between electrodes placed on the skin. Analysis of the time and voltage data give important parameters used to diagnose the above abnormalities and diseases.

## Overview
The input ECG data comes from a CSV file containing two columns of data: time and voltage. If either value in a `time, voltage` pair is missing, contains a string, or is NaN, an `ERROR` is logged, and the data pair is skipped. If a voltage value is found outside the normal range of +/- 300 mV, a `WARNING` is logged for the file. Starting analysis of a new trace and each dictionary value logs an `INFO` entry. The program analyzes the ECG strip to create a `metrics` dictionary with the following keys:
* `duration` (float): time duration of the ECG strip
* `voltage_extremes` (floats): tuple in the form `(min, max)` where `min` and `max`
    are the minimum and maximum lead voltages in the file    
* `num_beats` (int): number of detected beats in the strip
* `mean_hr_bpm` (int): average heart rate over the length of the strip  
* `beats` (list of floats): list of times when a beat occurred

This dictionary is then output as a JSON file for the data file.

### Defining and Identifying a Beat
Heart beats are identified via the Pan-Tompkins detector (https://github.com/berndporr/py-ecg-detectors) using the sampling period of the ECG strip (`fs = 1/(time[1]-time[0])`). The algorithm detects QRS complexes (waves in an ECG), which are composed of a downward deflection (Q), a high upward deflection (R), and another downward deflection (S). Via a series of filters (low-pass, high-pass, derivative), the characteristic rapid depolarization is highlighted and the background noise removed. The resulting filtered signal is then squared to amplify the QRS depolarization. Lastly, adaptive thresholds are applied to detect the signal peaks.
You can read more at <https://en.wikipedia.org/wiki/Pan%E2%80%93Tompkins_algorithm>.

### Calculating BPM
Heart rate is calculated as beats per minute. The duration of the ECG strip is converted to minutes via `min = sec/60`. The number of beats detected in the ECG strip is then divided by the duration in minutes (`bpm = numbeats/t_in_min`) and rounded to the nearest integer.

## Run Instructions
To analyze a certain ECG strip, open `ecg_analysis.py` and enter the path and filename of the desired file on the line ```file ='' ```. For this program, the test data file must be located in a folder.
For example, the file `test_data2.csv` is selected by inputting `file = 'test_data/test_data2.csv'`, where test_data is the folder that contains the file ```test_data2.csv```.

To run the program, input `python ecg_analysis.py` into the command line. 
A JSON file will be created for the ECG strip (`filename.json`, where filename = test_data2 following the above example file) with the analysis results in JSON format: `duration`, `voltage_extremes`, `num_beats`, `mean_hr_bpm`,  and `beats`.

## License
MIT License

Copyright (c) [2020] [Aimee McVey]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

More information on this assignment can be found at <https://github.com/dward2/BME547/tree/master/Assignments/ECG_Analysis>.
